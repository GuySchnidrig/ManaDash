# Import libraries
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import seaborn as sns
import matplotlib.colors as mcolors
from dash import dcc, html, Input, Output, callback_context, ALL, State
import plotly.express as px
import requests
from collections import defaultdict
import json

# Import local functions and pages
from backend.game_data import get_vintage_players

from dash_application_vintage.landing_page import create_landing_page

from dash_application_vintage.decks_page import create_decks_page
from dash_application_vintage.archetypes_page import create_archetypes_page
from dash_application_vintage.player_page import create_player_page
from dash_application_vintage.player_elo_page import create_player_elo_page 
from dash_application_vintage.data_page import create_standings_page

from backend.game_data import *


# Get data
initialize_data()

# Get player data
vintage_players_df = get_vintage_players()
vintage_decks_df = get_vintage_decks()

# Generate Player color mapping
unique_players = vintage_players_df['player'].unique()
palette = sns.color_palette("hls", len(unique_players), desat = 0.85)
color_list_p = [mcolors.to_hex(color) for color in palette]

player_color_map = dict(zip(unique_players, color_list_p))

# Generate Archetype color mapping
unique_archetypes = vintage_decks_df['archetype'].unique()
palette = sns.color_palette("hls", len(unique_archetypes), desat = 0.85)
color_list_a = [mcolors.to_hex(color) for color in palette]

archetype_color_map = dict(zip(unique_archetypes, color_list_a))

# Generate Decktype color mapping
unique_decktypes = vintage_decks_df['decktype'].unique()
palette = sns.color_palette("hls", len(unique_decktypes), desat = 0.85)
color_list_d = [mcolors.to_hex(color) for color in palette]

decktype_color_map = dict(zip(unique_decktypes, color_list_d))


# Dash APP
def create_dash_application_vintage(flask_app):
    dash_app = dash.Dash(server=flask_app, 
                         name="vintage_dash", 
                         url_base_pathname="/vintage/", 
                         suppress_callback_exceptions=True)
    
    # Set custom index string with favicon, but include required Dash placeholders
    dash_app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
            <title>ManaDash</title>
            {%metas%}
            {%css%}
        </head>
        <body>
            <div id="react-entry-point">
                {%app_entry%}
            </div>
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dbc.Navbar(
            dbc.Container(
                html.Div(
                    [
                        dbc.NavbarBrand(
                            [
                                html.Img(
                                    src="https://raw.githubusercontent.com/GuySchnidrig/ManaDash/868018bbeeabbd486be438a99f62744b0ec9c7de/icons/scroll-unfurled-svgrepo-com.svg",
                                    style={"width": "30px", "height": "30px"}
                                ),
                                html.Span("ManaDash", style={"margin-left": "8px"})
                            ],
                            href="/",
                        ),
                        dbc.Nav(
                            [
                                dbc.NavLink("Vintage Cube", href="/vintage/", active="exact"),
                                dbc.NavLink("Archetypes", href="/vintage/archetypes", active="exact"),
                                dbc.NavLink("Player", href="/vintage/player", active="exact"),
                                dbc.NavLink("Player-Elo", href="/vintage/player-elo", active="exact"),
                                dbc.NavLink("Decks", href="/vintage/decks", active="exact"),
                                dbc.NavLink("Standings", href="/vintage/standings", active="exact"),
                            ],
                            navbar=True,
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center", "justifyContent": "flex-start", "gap": "1rem"}
                ),
                fluid=True,
            ),
            color="primary",
            dark=True,
            className="sticky-top" 
        ),
        dcc.Loading(
        id="loading-spinner",
        type="default",  # Options: 'default', 'circle', 'dot', 'cube'
        fullscreen=False,
        children=html.Div(id='page-content', style={'position': 'relative', 'minHeight': '200px'})
    )
    ])
    

    # Callback to update the figure based on player selection
    @dash_app.callback(
        Output('archetype-plot', 'figure'),
        Output('decktype-plot', 'figure'),
        Output('filtered-stats-table', 'data'),
        Input('player-dropdown', 'value')
    )
    def update_player_data(selected_player_id):
        decks_with_standings = get_decks_with_standings()
        players_df = get_vintage_players()  # has player_id + player (name)
        decks_with_standings = decks_with_standings.merge(
        players_df[['player_id', 'player']], 
        on='player', 
        how='left'
        )
        game_stats = get_full_game_stats_table()
        
        if selected_player_id:
            filtered_decks = decks_with_standings[decks_with_standings['player_id'] == selected_player_id]
            filtered_stats = game_stats[game_stats['player_id'] == selected_player_id]
        else:
            filtered_decks = decks_with_standings
            filtered_stats = game_stats
        # Archetype
        summary_df_bar_archetype = (
            filtered_decks
            .groupby('archetype')
            .agg(arche_types_count=('deck_id', 'count'))
            .reset_index()
            .sort_values('arche_types_count', ascending=False)
        )
        
        archetype_fig = px.bar(
            summary_df_bar_archetype,
            x='archetype',
            y='arche_types_count',
            color='archetype',
            color_discrete_map=archetype_color_map,
            title='Archetypes',
            labels={'arche_types_count': 'Count', 'archetype': ''},
        )

        archetype_fig.update_layout(
            plot_bgcolor='white',
            showlegend=False
        )
        
        # Decktype
        summary_df_bar_decktype = (
            filtered_decks
            .groupby('decktype')
            .agg(decktype_counts=('deck_id', 'count'))
            .reset_index()
            .sort_values('decktype_counts', ascending=False)
        )

        decktype_fig = px.bar(
            summary_df_bar_decktype,
            x='decktype',
            y='decktype_counts',
            color='decktype',
            color_discrete_map=decktype_color_map,
            title='Decktypes',
            labels={'decktype_counts': 'Count', 'decktype': ''},
        )

        decktype_fig.update_layout(
            plot_bgcolor='white',
            showlegend=False
        )
        
        
        # Player Stats
        filtered_stats_summary = (
            filtered_stats
            .assign(is_win=lambda df: df['standing'] == 1)
            .groupby(['season_id', 'player_name'], as_index=False)
            .agg(
                archetype_count=('archetype', 'size'),
                total_wins=('is_win', 'sum'),
                total_points=('game_points', 'sum'),
                most_common_archetype=('archetype', lambda x: x.value_counts().idxmax()),
                most_common_decktype=('decktype', lambda x: x.value_counts().idxmax()),
                average_omp=('OMP', 'mean'),
                average_gwp=('GWP', 'mean'),
                average_ogp=('OGP', 'mean'),
            )
            .assign(
                win_percentage=lambda df: df['total_wins'] / df['archetype_count'] * 100
            )
            .sort_values(by='archetype_count', ascending=False)
        )


        filtered_stats_summary = filtered_stats_summary.to_dict('records')

        return archetype_fig, decktype_fig, filtered_stats_summary

    @dash_app.callback(
        Output('card-image-div', 'children'),  # Update div with the image
        Input('table', 'active_cell'),          # Detect the active cell (hovered row)
        Input('table', 'data'),                  # Get the table data
    )
    def update_card_image(active_cell, rows):
        if active_cell:
            # Get the row index from the active cell
            row_index = active_cell['row_id'] - 1
            card_name = rows[row_index]['card_name']
            
            # Fetch card details from Scryfall API using the card name
            url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
            response = requests.get(url)
            
            if response.status_code == 200:
                card_data = response.json()
                
                # Check if the card has multiple faces (e.g., double-faced cards)
                if 'image_uris' in card_data:
                    # Single-faced card, get the 'normal' image from 'image_uris'
                    first_image_url = card_data['image_uris'].get('normal', '')
                    second_image_url = None  # No second image in this case
                elif 'card_faces' in card_data:
                    # Multi-faced card, get images from 'card_faces'
                    faces = card_data['card_faces']
                    first_image_url = faces[0]['image_uris'].get('normal', '') if len(faces) > 0 else ''
                    second_image_url = faces[1]['image_uris'].get('normal', '') if len(faces) > 1 else ''
                else:
                    # Neither image_uris nor card_faces are found
                    first_image_url = ''
                    second_image_url = ''
                
                # Return the first image URL if available
                if first_image_url:
                    return html.Img(src=first_image_url, style={'width': '200px', 'height': 'auto'})
                else:
                    return "Image not available"
            else:
                return "Card not found"
        
        return "Hover over a card to view the image"
    
    @dash_app.callback(
    Output('deck-dropdown', 'options'),
    Output('deck-dropdown', 'value'),
    Input('player-dropdown', 'value')
    )
    
    def update_deck_dropdown(selected_player_id):
        if not selected_player_id:
            return [], None
        filtered_decks = vintage_decks_df[vintage_decks_df['player'] == selected_player_id]
        filtered_decks = filtered_decks.sort_values('deck_id', ascending=False)
        deck_options = [{'label': str(row['deck_id']), 'value': row['deck_id']} for _, row in filtered_decks.iterrows()]
        default_value = deck_options[0]['value'] if deck_options else None
        return deck_options, default_value
    
    # Callback to update card display and stats when player or deck changes
    @dash_app.callback(
        Output("creature-card-row", "children"),
        Output("noncreature-card-row", "children"),
        Output("stats-panel", "children"),
        Input("player-dropdown", "value"),
        Input("deck-dropdown", "value")
    )
    def update_card_rows(player, deck_id):
        if not player or not deck_id:
            return "", "", ""
        card_names = get_deck_card_names(player, deck_id)
        cards = [fetch_card_data(name) for name in card_names]
        cards = [c for c in cards if c]

        creatures = [c for c in cards if c["is_creature"]]
        non_creatures = [c for c in cards if not c["is_creature"]]

        stats = calculate_stats(cards)

        return render_row(group_by_cmc(creatures)), render_row(group_by_cmc(non_creatures)), render_stats_panel(stats)
    
    # Callback to display zoomed card on click
    @dash_app.callback(
        Output("zoomed-card-container", "children"),
        Input({"type": "card-image", "index": ALL}, "n_clicks"),
        State({"type": "card-image", "index": ALL}, "id")
    )
    
    def display_zoomed_card(n_clicks_list, ids):
        ctx = callback_context
        if not ctx.triggered:
            return "Click a card to zoom."

        triggered_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
        card_name = triggered_id["index"]
        card = fetch_card_data(card_name)
        if not card:
            return "Card not found."

        return html.Div([
            html.H6(card["name"]),
            html.Img(
                src=card["image_url"],
                style={
                    "width": "300px",
                    "border-radius": "12px",                    # rounded corners like MTG cards
                    "box-shadow": "0 4px 12px rgba(0,0,0,0.3)", # subtle shadow for depth
                    "border": "1px solid #ccc",                 # thin border for definition
                    "object-fit": "cover"                       # make sure image covers container nicely
                }
            )
        ])
    
    
    @dash_app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')],
    )
    def display_page(pathname):
        if pathname == '/vintage/player':
            return create_player_page(player_color_map, archetype_color_map, decktype_color_map)
        elif pathname == '/vintage/archetypes':
            return create_archetypes_page(player_color_map, archetype_color_map, decktype_color_map)
        elif pathname == '/vintage/decks':
            return create_decks_page(player_color_map, archetype_color_map, decktype_color_map)
        
        elif pathname == '/vintage/player-elo':
            return create_player_elo_page(player_color_map, archetype_color_map, decktype_color_map)

        elif pathname == '/vintage/standings':
            return create_standings_page()
        elif pathname == '/':
            return dcc.Location(pathname='/redirect_to_flask', id='redirect_to_flask')
        else:
            return create_landing_page(player_color_map, archetype_color_map)

    return dash_app

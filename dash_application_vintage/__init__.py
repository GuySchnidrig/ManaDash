# Import libraries
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import seaborn as sns
import matplotlib.colors as mcolors
from dash import dcc, html, Input, Output
import plotly.express as px
import requests

# Import local functions and pages
from backend.game_data import get_vintage_players

from dash_application_vintage.landing_page import create_landing_page
from dash_application_vintage.decks_page import create_decks_page
from dash_application_vintage.player_page import create_player_page
from dash_application_vintage.cards_page import create_cards_page

from dash_application_vintage.data_page import create_standings_page
from backend.game_data import get_vintage_players, get_decks_with_standings, get_vintage_decks

# Get player data
vintage_players_df = get_vintage_players()
vintage_decks_df = get_vintage_decks()

# Generate Player color mapping
unique_players = vintage_players_df['player_name'].unique()
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
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Vintage Cube", href="/vintage/"),
                dbc.NavLink("Decks", href="/vintage/decks"),
                dbc.NavLink("Player", href="/vintage/player"),
                dbc.NavLink("Cards", href="/vintage/cards"),
                dbc.NavLink("Standings", href="/vintage/standings")
            ],
            brand=[
                html.Img(
                    src="https://raw.githubusercontent.com/GuySchnidrig/ManaDash/868018bbeeabbd486be438a99f62744b0ec9c7de/icons/scroll-unfurled-svgrepo-com.svg",
                    style={"width": "30px", "height": "30px"}
                ),
                html.Span("ManaDash", style={"margin-left": "8px"})
            ],
            brand_href="/",
            color="primary",
            dark=True,
            className="navbar"  
        ),
        html.Div(id='page-content')
    ])
    

    # Callback to update the figure based on player selection
    @dash_app.callback(
        Output('archetype-plot', 'figure'),
        Output('filtered-decks-table', 'data'),
        Input('player-dropdown', 'value')
    )
    def update_archetype_fig(selected_player):
        # Load data again if necessary, or filter based on selected player
        decks_with_standings = get_decks_with_standings()

        if selected_player:
            filtered_decks = decks_with_standings[decks_with_standings['player_id'] == selected_player]
        else:
            filtered_decks = decks_with_standings

        # Aggregate data for the selected player
        summary_df_bar = (
            filtered_decks
            .groupby('archetype')
            .agg(arche_types_count=('deck_id', 'count'))
            .reset_index()
            .sort_values('arche_types_count', ascending=False)
        )

        # Create the updated figure
        archetype_fig = px.bar(
            summary_df_bar,
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
        # Prepare the data for the filtered decks table
        filtered_decks_data = filtered_decks.to_dict('records')
        return archetype_fig, filtered_decks_data

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
                card_image_url = card_data.get('image_uris', {}).get('normal', '')

                if card_image_url:
                    # Return the image in an <img> element
                    return html.Img(src=card_image_url, style={'width': '300px', 'height': 'auto'})
                else:
                    return "Image not available"
            else:
                return "Card not found"
        return "Hover over a card to view the image"
    
    @dash_app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')],
    )
    def display_page(pathname):
        if pathname == '/vintage/player':
            return create_player_page(player_color_map, archetype_color_map, decktype_color_map)
        elif pathname == '/vintage/decks':
            return create_decks_page(player_color_map, archetype_color_map, decktype_color_map)
        elif pathname == '/vintage/cards':
            return create_cards_page()
        elif pathname == '/vintage/standings':
            return create_standings_page()
        elif pathname == '/':
            return dcc.Location(pathname='/redirect_to_flask', id='redirect_to_flask')
        else:
            return create_landing_page(player_color_map, archetype_color_map)

    return dash_app

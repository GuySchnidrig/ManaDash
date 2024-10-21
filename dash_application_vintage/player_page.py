from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
from backend.game_data import get_vintage_players

def create_player_page(player_color_map, archetype_color_map, decktype_color_map):
    # Load data
    players_df = get_vintage_players()
    
    # Generate dropdown options from the DataFrame
    player_options = [
        {'label': row['player_name'], 'value': row['player_id']} 
        for _, row in players_df.iterrows()
    ]
    # Set default value to the first player's ID if available
    default_player_id = player_options[0]['value'] if player_options else None
    
    # Initial empty figure
    archetype_fig = px.bar(title='Archetypes')

    # Sidebar for player selection
    sidebar = dbc.Col(
        [
            html.H4("Select Player"),
            dcc.Dropdown(
                id='player-dropdown',
                options=player_options,
                value=default_player_id,  # Set default value here
                placeholder="Choose a player",
                style={'margin-bottom': '20px'}
            ),
        ],
        width=3,  # Set width to fit your design (25% of the container)
        style={'padding': '20px'}
    )

    # Main content area for displaying the plots and table
    content = dbc.Col(
        html.Div([
            dcc.Graph(id='archetype-plot', figure=archetype_fig,
                      config={'displayModeBar': False}),  # This hides the mode bar
            dcc.Graph(id='archetype-plot2', figure=archetype_fig,
                      config={'displayModeBar': False}),
            dcc.Graph(id='archetype-plot3', figure=archetype_fig,
                      config={'displayModeBar': False}),
            dash_table.DataTable(
                id='filtered-decks-table',
                columns=[
                    {'name': 'Date', 'id': 'date'},
                    {'name': 'Deck ID', 'id': 'deck_id'},
                    {'name': 'Player ID', 'id': 'player_id'},
                    {'name': 'Archetype', 'id': 'archetype'},
                    # Add more columns as needed based on your DataFrame
                ],
                data=[],  # Initial empty data, will be filled by callback
                page_size=10,  # Adjust page size if needed
            ),
        ]),
        width=9,  # Set width to fit your design (75% of the container)
        style={'padding': '20px'}
    )

    # Combine sidebar and content into a single layout
    layout = dbc.Container(
        [
            dbc.Row([sidebar, content])  # Both sidebar and content in the same row
        ],
        fluid=True  # Use fluid layout for better responsiveness
    )

    return layout
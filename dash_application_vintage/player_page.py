from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
from backend.game_data import get_vintage_players

def create_player_page(player_color_map, archetype_color_map, decktype_color_map):
    # Load data
    players_df = get_vintage_players()
    

    # Generate dropdown options from the DataFrame
    player_options = [
        {'label': row['player'], 'value': row['player_id']}
        for _, row in players_df.iterrows()
    ]
    # Set default value to the first player's ID if available
    default_player_id = player_options[0]['value'] if player_options else None
    
    # Initial empty figure
    archetype_fig = px.bar(title='Archetypes')
    decktype_fig = px.bar(title='Decktypes')

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
        width=2,  
        style={'padding': '20px', 'max-width': '200px'}  # Set max-width for sidebar
    )

    # Main content area for displaying the plots and table
    content = dbc.Col(
        html.Div([
            html.H3("Player Statistics Overview", style={'textAlign': 'left'}),
            
            html.Div(
                dash_table.DataTable(
                    id='filtered-stats-table',
                    columns=[
                        {'name': 'Season', 'id': 'season_id'},
                        {'name': 'Player', 'id': 'player_id'},
                        {'name': 'Wins', 'id': 'total_wins', 'type': 'numeric'},
                        {'name': 'Win Percentage', 'id': 'win_percentage', 'type': 'float'},
                        {'name': 'Total Points', 'id': 'total_points', 'type': 'numeric'},
                        {'name': 'Most Common Archetype', 'id': 'most_common_archetype'},
                        {'name': 'Most Common Decktype', 'id': 'most_common_decktype'},
                        {'name': 'Average OMP', 'id': 'average_omp', 'type': 'float'},
                        {'name': 'Average GWP', 'id': 'average_gwp', 'type': 'float'},
                        {'name': 'Average OGP', 'id': 'average_ogp', 'type': 'float'},
                    ],
                    data=[],  # Initial empty data, will be filled by callback
                    page_size=10,  # Adjust page size if needed
                    style_table={'overflowX': 'auto'},  # Allow horizontal scrolling
                    style_cell={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'minWidth': '100px',  # Minimum width for cells
                        'maxWidth': '300px',  # Maximum width for cells
                    },
                    style_header={
                        'backgroundColor': 'lightgrey',
                        'fontWeight': 'bold'
                    },
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    }
                ),
                style={'overflowX': 'auto'}  # Allow overflow for the table
            ),
            
            dcc.Graph(id='archetype-plot', figure=archetype_fig,
                      config={'displayModeBar': False}),  # This hides the mode bar
            
            dcc.Graph(id='decktype-plot', figure=decktype_fig,
                      config={'displayModeBar': False})
        ]),
        width=9,  
        style={'padding': '20px'}
    )

    # Combine sidebar and content into a single layout
    layout = dbc.Container(
        [
            dbc.Row([sidebar, content], align='start')  # Align items at the start
        ],
        fluid=True  # Use fluid layout for better responsiveness
    )

    return layout
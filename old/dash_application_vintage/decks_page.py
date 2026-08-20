# Import libraries
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from backend.game_data import *

def create_decks_page(player_color_map, archetype_color_map, decktype_color_map):
    decks_df = get_data('decktype_game_winrate')
    
    # Check which column name exists in the dataframe
    decktype_column = 'deck_type' if 'deck_type' in decks_df.columns else 'decktype'
    
    # Sort the DataFrame by 'games_played' in descending order
    sorted_game_data_df = decks_df.sort_values(by='games_played', ascending=False)
    
    return html.Div([  
        dash_table.DataTable(
            id='deck-stats-table',
            sort_action='native',
            filter_action='native',
            filter_options={'case': 'insensitive'},
            columns=[
                {'name': 'Season', 'id': 'season_id'},
                {'name': 'Deck Type', 'id': decktype_column},
                {'name': 'Games Won', 'id': 'games_won', 'type': 'numeric'},
                {'name': 'Games Played', 'id': 'games_played', 'type': 'numeric'},
                {'name': 'Game Win Rate', 'id': 'game_winrate', 'type': 'numeric', 'format': {'specifier': '.2f'}}
            ],
            data=sorted_game_data_df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'minWidth': '100px',
                'maxWidth': '300px',
            },
            style_header={
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            }
        )
    ])
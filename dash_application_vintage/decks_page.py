# Import libraries
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

from backend.game_data import *

# Import local functions and pages

def create_decks_page(player_color_map, archetype_color_map, decktype_color_map):
    decks_df = get_data('decktype_game_winrate')
    
    # Sort the DataFrame by 'games_played' in descending order (you can adjust if necessary)
    sorted_game_data_df = decks_df.sort_values(by='games_played', ascending=False)

    # Prepare the columns for the DataTable
    columns = [{'name': col, 'id': col} for col in sorted_game_data_df.columns]

    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=columns,  # Set the columns here
            data=sorted_game_data_df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            sort_action='native',
            filter_action='native',
            filter_options={'case':'insensitive'},
            style_cell={
                'textAlign': 'left',
                'padding': '5px'
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
        )
    ])

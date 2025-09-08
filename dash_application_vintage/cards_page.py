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

def create_cards_page(player_color_map, archetype_color_map, decktype_color_map):
    cards_df = get_data('card_game_winrate_per_season')
    
    # Sort the DataFrame by 'games_played' in descending order (you can adjust if necessary)
    sorted_game_data_df = cards_df.sort_values(by='games_played', ascending=False)

    # Round
    sorted_game_data_df["game_win_rate"] = sorted_game_data_df["game_win_rate"].round(2)

    # List of columns to drop
    drop_cols = [
        "season_id",
        "scryfallId"

    ]

    # Drop them
    sorted_game_data_df = sorted_game_data_df.drop(columns=drop_cols)

    # Numeric cols   
    numeric_cols = [

    "games_played",
    "games_won",
    "game_win_rate"
    ]

    # Reorder cols
    sorted_game_data_df = sorted_game_data_df[["card_name", "games_won", "games_played", "game_win_rate"]]

    # Force numeric conversion again to be sure
    for col in numeric_cols:
        sorted_game_data_df[col] = pd.to_numeric(sorted_game_data_df[col], errors="coerce")
    
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
            }
        )
    ])

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

def create_standings_page():
    vintage_standings_df = get_vintage_standings()

    # Sort the DataFrame by 'draft_id' in descending order (you can adjust if necessary)
    sorted_game_data_df = vintage_standings_df.sort_values(by='draft_id', ascending=False)

    # Apply labels
    sorted_game_data_df = add_season_draft_labels(sorted_game_data_df)

    # List of columns to drop
    drop_cols = [
        "season_id",
        "player_id",
        "byes",
        "draft_id",
        "season_num",
        "d_in_season",
        "matches_played"
    ]

    # Drop them
    sorted_game_data_df = sorted_game_data_df.drop(columns=drop_cols)

    # Numeric cols   
    numeric_cols = [
    
    "match_points",
    "standing",
    "game_points",
    "games_played",
    "MWP",
    "OMP",
    "GWP",
    "OGP",
    ]

    # Force numeric conversion again to be sure
    for col in numeric_cols:
        sorted_game_data_df[col] = pd.to_numeric(sorted_game_data_df[col], errors="coerce")

    # Reorder with col first
    sorted_game_data_df = sorted_game_data_df[["season_draft_label"] + [c for c in sorted_game_data_df.columns if c != "season_draft_label"]]

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

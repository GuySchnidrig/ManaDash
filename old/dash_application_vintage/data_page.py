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

    # Reorder with col first
    sorted_game_data_df = sorted_game_data_df[["season_draft_label"] + [c for c in sorted_game_data_df.columns if c != "season_draft_label"]]

    return html.Div([
        dash_table.DataTable(
            id='full-game-stats-table',
            sort_action='native',
            filter_action='native',
            filter_options={'case': 'insensitive'},
            columns=[
                {'name': 'Draft ID', 'id': 'season_draft_label'},
                {'name': 'Player', 'id': 'player'},
                {'name': 'Match Points', 'id': 'match_points', 'type': 'numeric'},
                {'name': 'Standing', 'id': 'standing', 'type': 'numeric'},
                {'name': 'Game Points', 'id': 'game_points', 'type': 'numeric'},
                {'name': 'Games Played', 'id': 'games_played', 'type': 'numeric'},
                {'name': 'Match Win % (MWP)', 'id': 'MWP', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': 'Opp Match Win % (OMP)', 'id': 'OMP', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': 'Game Win % (GWP)', 'id': 'GWP', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                {'name': 'Opp Game Win % (OGP)', 'id': 'OGP', 'type': 'numeric', 'format': {'specifier': '.2f'}}
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

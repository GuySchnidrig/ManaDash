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

from backend.game_data import get_full_game_stats_table

# Import local functions and pages

def create_standings_page():
    vintage_standings_df = get_full_game_stats_table()
    
    # Sort the DataFrame by 'draft_id' in descending order (you can adjust if necessary)
    sorted_game_data_df = vintage_standings_df.sort_values(by='draft_id', ascending=False)

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

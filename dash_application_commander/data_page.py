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

# Import local functions and pages
from backend.game_data import get_games

def create_game_data_page(game_data_df):
    sorted_game_data_df = game_data_df.sort_values(by='id', ascending=False)
    columns_to_hide = {'uploader', 'color'}    
    visible_columns = [col for col in game_data_df.columns if col not in columns_to_hide]

    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in visible_columns],
            data=sorted_game_data_df[visible_columns].to_dict('records'),
            style_table={'overflowX': 'auto'},  
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

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

def create_game_data_page(vintage_standings_df):
    # Sort the DataFrame by 'draft_id' in descending order
    sorted_game_data_df = vintage_standings_df.sort_values(by='draft_id', ascending=False)

    # Prepare the columns for the DataTable
    columns = [{'name': col, 'id': col} for col in sorted_game_data_df.columns]

    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=columns,  # Set the columns here
            data=sorted_game_data_df.to_dict('records'),
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

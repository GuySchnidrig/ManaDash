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
import requests
from dash.dependencies import Input, Output

from backend.game_data import get_all_cards

# Import local functions and pages

def create_cards_page():
    cards_df = get_all_cards()
    sorted_game_data_df = cards_df.sort_values(by='card_id', ascending=True)
    
    columns = [{'name': col, 'id': col} for col in sorted_game_data_df.columns]
    sorted_game_data_df['id'] = sorted_game_data_df['card_id'] 
        
    return html.Div(
        style={'display': 'flex', 'alignItems': 'flex-start'},  # Flexbox layout
        children=[
            dash_table.DataTable(
                id='table',
                columns=columns,
                data=sorted_game_data_df.to_dict('records'),
                page_size= 25,
                sort_action='native',
                filter_action='native',
                filter_options={'case':'insensitive'},
                style_table={'overflowX': 'auto', 'flex': '1'},  # Allow table to take available space
                style_cell={
                    'textAlign': 'left',
                    'padding': '5px'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                
                # Enable row hover functionality
                style_data_conditional=[
                    {
                        'if': {'state': 'hover'},  # When hovered over
                        'backgroundColor': 'rgba(255, 255, 255)',
                        'border': '1px solid black'
                    }
                ]
            ),
                    html.Div(
                id='card-image-div',
                style={
                    'flex': '0 0 310px',  # Fixed width for the image div  Space for displaying the card image
                    'padding': '10px',
                    'overflow': 'hidden'  # Prevent overflow of content
                }
            ) 
        ]
    )
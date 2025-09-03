# Import libraries
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import seaborn as sns
import matplotlib.colors as mcolors
from dash import dcc, html, Input, Output, callback_context, ALL, State
import plotly.express as px
import requests
from collections import defaultdict
import json

# Import local functions and pages
from backend.game_data import *

# Get data
initialize_data()

# Generate Player color mapping



# Load data
players_df = get_vintage_players()


player_options = [
    {'label': row['player'], 'value': row['player_id']}
    for _, row in players_df.iterrows()
]

# Set default value to the first player's ID if available
default_player_id = player_options[0]['value'] if player_options else None


# Initial empty figure
archetype_fig = px.bar(title='Archetypes')
decktype_fig = px.bar(title='Decktypes')

print(archetype_fig)
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

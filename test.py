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
players_df = get_vintage_players()


player_options = [
    {'label': row['player'], 'value': row['player_id']}
    for _, row in players_df.iterrows()
]


# Set default value to the first player's ID if available
default_player_id = player_options[0]['value'] if player_options else None


decks_with_standings = get_decks_with_standings()

selected_player_id = 1
filtered_decks = decks_with_standings[decks_with_standings['player_id'] == selected_player_id]


game_stats = get_full_game_stats_table()
filtered_stats = game_stats[game_stats['player_id'] == selected_player_id]

sample_player_id = 10      # 👈 replace with a real player_id from your data
sample_deck_id = 3    # 👈 replace with a real draft_id/deck_id from your data




names = get_deck_card_names(sample_player_id, sample_deck_id)
print(names)
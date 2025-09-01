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

# Get player data
vintage_players_df = get_vintage_players()
vintage_drafts_df = get_vintage_drafts()
vintage_standings_df = get_vintage_standings()
vintage_decks_df = get_vintage_decks()
vintage_players_df = get_vintage_players()


# Generate Player color mapping
players_df = get_vintage_players()
print(players_df)

player_options = [
    {'label': row['player'], 'value': row['player_id']} 
    for _, row in players_df.iterrows()
]

print(player_options)

decks_with_standings = get_decks_with_standings()
game_stats = get_full_game_stats_table()

print(decks_with_standings)
print(game_stats)

selected_player_id = 1
filtered_stats = game_stats[game_stats['player_id'] == selected_player_id]
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




player_elo_df = get_player_elo()

player_elo_df = (
    player_elo_df
    .sort_values(['player', 'draft_id'])      # ensures proper order
    .groupby(['player', 'draft_id'], as_index=False)
    .last()  # or .tail(1) per group
)

player_elo_df = player_elo_df[
        (player_elo_df['player'].notna()) &
        (player_elo_df['player'] != "") &
        (player_elo_df['player'] != "0")
    ]

initial_players = ['Dimlas', 'Andrin','Dimlas ', 'Sili', 'Manuel', 'Lukas Stalder', 'Tommy', 'Noe', 'Guy', 'Ivo']
player_elo_df['draft_id'] = player_elo_df['draft_id'].astype(str)

fig = px.line(
    player_elo_df,
    x='draft_id',
    y='elo',
    color='player',
    title='Player ELO Over Time',
    labels={'elo': 'ELO Rating', 'draft_id': 'Draft', 'player': 'Player'},
    line_shape='spline'
)

# Set trace visibility based on initial_players
if initial_players is not None:
    for trace in fig.data:
        # trace.name holds the player here
        if trace.name in initial_players:
            trace.visible = True
        else:
            trace.visible = 'legendonly'

fig.add_hline(
    y=1000,
    line_dash="dot",
    line_color="red",
    line_width=3,
    annotation_text="ELO = 1000",
    annotation_position="top right"
)

fig.update_layout(
    plot_bgcolor='white',
    xaxis=dict(tickmode='linear', tickangle=45),
    margin=dict(l=20, r=20, t=50, b=20),
    height=600
)

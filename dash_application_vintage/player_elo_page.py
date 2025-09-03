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
import json

# Import local functions and pages
from backend.game_data import *

def create_player_elo_page(player_color_map, archetype_color_map, decktype_color_map):
    
    player_elo_df = get_player_elo()
    
    # Get latest elo entry
    player_elo_df = (
    player_elo_df
    .sort_values(['player', 'draft_id'])      
    .groupby(['player', 'draft_id'], as_index=False)
    .last()  
    )

    # Remove Buy and NA
    player_elo_df = player_elo_df[
        (player_elo_df['player'].notna()) &
        (player_elo_df['player'] != "") &
        (player_elo_df['player'] != "Missing Player")
        ]
    
    # Set intial players
    initial_players = ['Dimlas', 'Andrin', 'Sili', 'Manuel', 'Lukas Stalder', 'Tommy', 'Noe', 'Guy', 'Ivo']
    
    # Convert draft_date to datetime if possible (replace with actual date format if needed)
    # Sort by draft_id as integer
    player_elo_df['draft_id'] = player_elo_df['draft_id'].astype(int)
    player_elo_df = player_elo_df.sort_values(['draft_id'])

    # Convert back to string for categorical axis
    player_elo_df['draft_id_str'] = player_elo_df['draft_id'].astype(str)

    fig = px.line(
        player_elo_df,
        x='draft_id_str',  # use string version
        y='elo',
        color='player',
        color_discrete_map=player_color_map,
        title='Player ELO Over Time',
        labels={'elo': 'ELO Rating', 'draft_id_str': 'Draft Date', 'player': 'Player'},
        line_shape='spline',
        category_orders={'draft_id_str': list(player_elo_df['draft_id_str'].unique())}  # enforce order
)

    # Set trace visibility based on initial_players
    if initial_players is not None:
        for trace in fig.data:
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
        xaxis=dict(
            tickformat="%Y-%m-%d", 
            tickangle=45
        ),
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=50, b=20),
        height=600
    )
    
    fig.update_xaxes(tickangle=45)
    
    return html.Div([
        dcc.Graph(
            figure=fig,
            config={'displayModeBar': False},
            style={'width': '100vw', 'height': '80vh'}
        )
    ],
    style={'width': '100vw', 'height': '100vh', 'margin': '0', 'padding': '0'})

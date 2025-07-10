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
from backend.game_data import get_vintage_standings
from backend.game_data import get_vintage_decks
from backend.game_data import get_decks_with_standings
from backend.game_data import get_vintage_players
from backend.game_data import get_player_elo

def create_player_elo_page(player_color_map, archetype_color_map, decktype_color_map):
    
    player_elo_df = get_player_elo()
    initial_players = ['Dimlas', 'Andrin','Dimlas ', 'Sili', 'Manuel', 'Lukas Stalder', 'Tommy', 'Noe', 'Guy', 'Ivo']
    player_elo_df['draft_id'] = player_elo_df['draft_id'].astype(str)
    
    fig = px.line(
        player_elo_df,
        x='draft_id',
        y='elo',
        color='player_name',
        color_discrete_map=player_color_map,
        title='Player ELO Over Time',
        labels={'elo': 'ELO Rating', 'draft_id': 'Draft', 'player_name': 'Player'},
        line_shape='spline'
    )
    
    # Set trace visibility based on initial_players
    if initial_players is not None:
        for trace in fig.data:
            # trace.name holds the player_name here
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
    
    return html.Div([
        dcc.Graph(
            figure=fig,
            config={'displayModeBar': False},
            style={'width': '100vw', 'height': '80vh'}
        )
    ],
    style={'width': '100vw', 'height': '100vh', 'margin': '0', 'padding': '0'})

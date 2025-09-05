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
    
    # Sort by season_id and draft_id
    player_elo_df = player_elo_df.sort_values(['season_id', 'draft_id'])

    # Extract numeric season if needed
    player_elo_df['season_num'] = player_elo_df['season_id'].astype(str).str.extract(r'(\d+)').astype(int)

    # Get unique draft_ids per season and assign D numbers
    draft_counts = (
        player_elo_df[['season_num', 'draft_id']]
        .drop_duplicates()  # unique draft_ids only
        .sort_values(['season_num', 'draft_id'])
        .groupby('season_num')
        .cumcount() + 1  # D1, D2, ...
    )
    # Map back to the original dataframe
    player_elo_df = player_elo_df.merge(
        player_elo_df[['season_num', 'draft_id']].drop_duplicates().assign(d_in_season=draft_counts),
        on=['season_num', 'draft_id'],
        how='left'
    )

    # Create S*D* label
    player_elo_df['season_draft_label'] = player_elo_df.apply(
        lambda row: f"S{row['season_num']}D{row['d_in_season']}", axis=1
    )

    # Set intial players
    initial_players = ['Dimlas', 'Andrin', 'Sili', 'Manuel', 'Lukas Stalder', 'Tommy', 'Noe', 'Guy', 'Ivo']
    
    fig = px.line(
        player_elo_df,
        x='season_draft_label',  
        y='elo',
        color='player',
        color_discrete_map=player_color_map,
        title='Player ELO Over Time',
        labels={'elo': 'ELO Rating', 'season_draft_label': 'Draft', 'player': 'Player'},
        line_shape='spline',
        category_orders={'season_draft_label': list(player_elo_df['season_draft_label'].unique())}  # enforce order
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
    
    # Transparent lines at 1100 and 1200
    fig.add_hline(
        y=1100,
        line_dash="dot",
        line_color="rgba(0,0,0,0.2)",  # semi-transparent black
        line_width=2,
        annotation_text="ELO = 1100",
        annotation_position="top right"
    )

    fig.add_hline(
        y=1200,
        line_dash="dot",
        line_color="rgba(0,0,0,0.2)",  # semi-transparent black
        line_width=2,
        annotation_text="ELO = 1200",
        annotation_position="top right"
    )

    fig.update_layout(
        xaxis=dict(
            tickangle=0  # horizontal labels
        ),
        plot_bgcolor='white',
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

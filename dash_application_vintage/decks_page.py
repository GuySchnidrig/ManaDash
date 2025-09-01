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


def create_decks_page(player_color_map, archetype_color_map, decktype_color_map):
    
    vintage_decks_df = get_vintage_decks()
    decks_with_standings = get_decks_with_standings()
    
    # Load data
    players_df = get_vintage_players()
    
    # Generate dropdown options from the DataFrame
    player_options = [
        {'label': row['player'], 'value': row['player_id']} 
        for _, row in players_df.iterrows()
    ]
    # Set default value to the first player's ID if available
    default_player_id = player_options[0]['value'] if player_options else None

    # Sidebar for player selection
    sidebar = dbc.Col(
        [
            html.H4("Select Player"),
            dcc.Dropdown(
                id='player-dropdown',
                options=player_options,
                value=default_player_id,
                placeholder="Choose a player",
                style={'margin-bottom': '20px'}
            ),
            html.H5("Player's Decks"),
            dcc.Dropdown(
                id='deck-dropdown',
                options=[],
                placeholder="Choose a deck",
                style={'margin-bottom': '10px'}
            )
        ],
        width=2,
        style={'padding': '20px', 'max-width': '250px', 'margin-bottom': '10px'}
    )

    # Deck Stats & Zoomed Card aligned with sidebar, width 2 or 3
    deck_stats_col = dbc.Col(
        [
            html.H5("Deck Stats", style={"marginBottom": "1rem"}),
            html.Div(id="stats-panel"),
        ]
            ,
        width=2,
        style={'padding': '20px', 'margin-bottom': '10px'}
    )
      
    zoom_card = dbc.Col(
        [
            html.Div(id="zoomed-card-container", className="text-center mt-3"),
        ],
        width=2,
        style={
            'padding': '0px',
            'margin-bottom': '-60px',  # Pull down the zoom card to overlap
            'z-index': 10,             # Ensure it's above the second row
            'position': 'relative'
        }
    )

    # Cards rows (creatures + noncreatures) below both sidebar and deck stats
    cards_rows = dbc.Col(
        [
            html.Div(id="creature-card-row", style={'marginBottom': '20px'}),
            html.Div(id="noncreature-card-row"),
        ],
        width=12,  # or 12 to stretch full width below
        style={'margin-top': '-20px', 'padding': '0px'}
    )

    # Layout structure:
    layout = dbc.Container(
        [
            dbc.Row(
                [
                    sidebar,          # width=2
                    deck_stats_col,   # width=2
                    #dbc.Col([], width=6),  # spacer pushes zoom_card to right
                    #zoom_card         # width=2
                ],
                align='start',
                className="mb-3"
            ),

            dbc.Row(
                [
                    dbc.Col(cards_rows, width=12)  # full width below
                ]
            )
        ],
        fluid=True
    )

    return layout
    
# Import libraries
from flask import Flask, render_template, request,redirect, url_for, session, flash, g
import os
import json
from flask_bootstrap import Bootstrap
from flask import redirect, url_for, session, request

# Import routings
# import commander
# import cube
import backend.player as player

# Import dash applications
from dash_application_commander import create_dash_application_commander
from dash_application_vintage import create_dash_application_vintage

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


import sqlite3
import pandas as pd
import os
import requests
from dash import callback_context, Input, Output, State, ALL, html
import dash_bootstrap_components as dbc
from collections import defaultdict
import json

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
from backend.game_data import get_vintage_players

from dash_application_vintage.landing_page import create_landing_page


from dash_application_vintage.decks_page import create_decks_page
from dash_application_vintage.archetypes_page import create_archetypes_page
from dash_application_vintage.player_page import create_player_page
from dash_application_vintage.player_elo_page import create_player_elo_page 
from dash_application_vintage.data_page import create_standings_page
from backend.game_data import get_vintage_players, get_decks_with_standings, get_vintage_decks, get_full_game_stats_table, get_deck_card_names, fetch_card_data, group_by_cmc, render_row, calculate_stats, render_stats_panel

# Get player data
vintage_players_df = get_vintage_players()
vintage_decks_df = get_vintage_decks()

# Generate Player color mapping
unique_players = vintage_players_df['player_name'].unique()
palette = sns.color_palette("hls", len(unique_players), desat = 0.85)
color_list_p = [mcolors.to_hex(color) for color in palette]

player_color_map = dict(zip(unique_players, color_list_p))

# Generate Archetype color mapping
unique_archetypes = vintage_decks_df['archetype'].unique()
palette = sns.color_palette("hls", len(unique_archetypes), desat = 0.85)
color_list_a = [mcolors.to_hex(color) for color in palette]

archetype_color_map = dict(zip(unique_archetypes, color_list_a))

# Generate Decktype color mapping
unique_decktypes = vintage_decks_df['decktype'].unique()
palette = sns.color_palette("hls", len(unique_decktypes), desat = 0.85)
color_list_d = [mcolors.to_hex(color) for color in palette]

decktype_color_map = dict(zip(unique_decktypes, color_list_d))
# Get player data
vintage_players_df = get_vintage_players()
vintage_decks_df = get_vintage_decks()

# Define the path to your SQLite database relative to the root of your project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one directory
DB_PATH = os.path.join(ROOT_DIR, 'data', 'cmdr_tracker_v2.db')

DB_PATH_vintage = os.path.join(ROOT_DIR, 'data', 'vintage_cube.db')
def get_games():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = "SELECT * FROM game_data"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df


def get_vintage_drafts():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = "SELECT * FROM drafts"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df

def get_player_elo():
    try:
        with sqlite3.connect(DB_PATH_vintage) as db:
            query = """
                SELECT pe.id,
                       pe.player_id,
                       p.player_name,
                       pe.draft_id,
                       pe.elo
                FROM player_elo pe
                LEFT JOIN Players p ON pe.player_id = p.player_id
            """
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()

player_elo_df = get_player_elo()
print(player_elo_df)
import sqlite3
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.colors as mcolors
import requests
from dash import html



# Define the path to your SQLite database relative to the root of your project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one directory
DB_PATH = os.path.join(ROOT_DIR, 'data', 'cmdr_tracker_v2.db')

DB_PATH_vintage = os.path.join(ROOT_DIR, 'data', 'vintage_cube.db')

def get_vintage_decks():
    try:
        with sqlite3.connect(DB_PATH_vintage) as db:
            query = """
            SELECT d.*, s.player_id AS player_id
            FROM decks d
            LEFT JOIN draft_standing s
                ON d.deck_id = s.deck_id
            """
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()
    return df


vintage_decks_df = get_vintage_decks()


# Display the improved summary table
print(vintage_decks_df)
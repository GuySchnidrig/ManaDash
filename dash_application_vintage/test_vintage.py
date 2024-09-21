import sqlite3
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.colors as mcolors


# Define the path to your SQLite database relative to the root of your project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one directory
DB_PATH = os.path.join(ROOT_DIR, 'data', 'cmdr_tracker_v2.db')

DB_PATH_vintage = os.path.join(ROOT_DIR, 'data', 'vintage_cube.db')

def get_vintage_decks():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = "SELECT * FROM decks"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df
vintage_decks_df = get_vintage_decks()

unique_decktypes = vintage_decks_df['decktype'].unique()
palette = sns.color_palette("hls", len(unique_decktypes), desat = 0.85)
color_list_d = [mcolors.to_hex(color) for color in palette]

decktype_color_map = dict(zip(unique_decktypes, color_list_d))

print(decktype_color_map)




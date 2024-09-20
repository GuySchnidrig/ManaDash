import sqlite3
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.colors as mcolors

# Define the path to your SQLite database relative to the root of your project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one directory
DB_PATH_vintage = os.path.join(ROOT_DIR, 'data', 'vintage_cube.db')

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

def get_vintage_standings():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = "SELECT * FROM draft_standing"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df

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

def get_vintage_players():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df

vintage_players_df = get_vintage_players()

print(len(vintage_players_df['player_name'].unique()))
print(vintage_players_df.columns)

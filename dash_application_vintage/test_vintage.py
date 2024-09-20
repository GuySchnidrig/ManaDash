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

def get_full_game_stats_table():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = """
                SELECT drafts.date,
                       drafts.season_id,
                       players.player_name,  
                       archetype, decktype, 
                       draft_standing.draft_id,draft_standing.standing, 
                       draft_standing.points, draft_standing.omp, 
                       draft_standing.gwp, draft_standing.ogp
                       
                FROM decks
                JOIN draft_standing ON decks.deck_id = draft_standing.deck_id
                JOIN players ON draft_standing.player_id = players.player_id
                JOIN drafts ON draft_standing.draft_id = drafts.draft_id
            """
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df


TSE = get_full_game_stats_table()


print(TSE)




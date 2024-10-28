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

def get_full_game_stats_table():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = """
                SELECT drafts.date,
                       drafts.season_id,
                       players.player_name,  
                       players.player_id,
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


# archtype win percentage plot
filtered_stats = get_full_game_stats_table()

# Create a summary table for player statistics
filtered_stats_summary = (
    filtered_stats
    .assign(
        is_win=lambda df: df['standing'] == 1  # Create a boolean column for wins
    )
    .groupby(['season_id','player_id', 'player_name'], as_index=False)
    .agg(
        archetype_count=('archetype', 'size'),  # Count each archetype occurrence
        total_wins=('is_win', 'sum'),  # Sum the wins for each archetype
        total_points=('points', 'sum'),  # Sum the total points

        most_common_archetype=('archetype', lambda x: x.value_counts().idxmax()),  # Most common archetype
        most_common_decktype=('decktype', lambda x: x.value_counts().idxmax()),  # Most common archetype
        average_omp=('omp', 'mean'),  # Average OMP
        average_gwp=('gwp', 'mean'),  # Average GWP
        average_ogp=('ogp', 'mean'),  # Average OGP
    )
    .assign(
        win_percentage=lambda df: df['total_wins'] / df['archetype_count'] * 100  # Calculate win percentage
    )
    .sort_values(by='archetype_count', ascending=False)  # Sort by count of archetypes
)

# Display the improved summary table
print(filtered_stats_summary)
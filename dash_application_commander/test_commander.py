import sqlite3
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.colors as mcolors

# Define the path to your SQLite database relative to the root of your project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one directory
DB_PATH = os.path.join(ROOT_DIR, 'data', 'cmdr_tracker.db')

def get_games():
    try:
        with sqlite3.connect(DB_PATH) as db:
            query = "SELECT * FROM game_data"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()
    return df

def validate_columns(df, required_columns):
    return all(col in df.columns for col in required_columns)

# Fetch data and validate
game_data_df = get_games()
required_columns = ['player_name', 'game_id']
if not validate_columns(game_data_df, required_columns):
    raise ValueError(f"DataFrame is missing required columns: {required_columns}")

# Generate color mapping
unique_players = game_data_df['player_name'].unique()
palette = sns.color_palette("hls", len(unique_players))
color_list = [mcolors.to_hex(color) for color in palette]

player_color_map = dict(zip(unique_players, color_list))

# Create summary DataFrame
game_data_df_pie = game_data_df[game_data_df['win'] == 1]  # Filter for wins
summary_df_pie = game_data_df_pie.groupby(['player_name']).agg(Games_won=('game_id', 'count')).reset_index()

summary_df_bar = game_data_df.groupby(['player_name']).agg(Played_Games=('game_id', 'count')).reset_index()
summary_df_bar = summary_df_bar.sort_values('Played_Games', ascending=False)

# Print color mapping for debugging

print(player_color_map)


# Create and show pie chart
fig = px.pie(
    summary_df_pie,
    names='player_name',
    values='Games_won',
    color='player_name',
    color_discrete_map=player_color_map,
    title='Total Games Won '
)

# Update layout to set white background and remove the legend
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=True,  # Set to True if you want to keep the legend
    legend_title_text='Player Name'
)

fig1 = px.bar(
        summary_df_bar,
        x='player_name',
        y='Played_Games',
        color='player_name',
        color_discrete_map=player_color_map,
        title='Number of Games Played by Each Player',
        labels={'Played_Games': 'Number of Games', 'player_name': 'Player Name'}
        )

fig1.update_layout(
    plot_bgcolor='white',
    showlegend=False,)

fig.show()
fig1.show()

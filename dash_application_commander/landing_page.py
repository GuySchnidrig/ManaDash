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

# Import local functions and pages
from backend.game_data import get_games


def create_landing_page(game_data_df, player_color_map):
    df = pd.DataFrame(
        {
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
        }
    )

    # Create summary DataFrame
    summary_df_bar = game_data_df.groupby(['player_name']).agg(Played_Games=('game_id', 'count')).reset_index()
    summary_df_bar = summary_df_bar.sort_values('Played_Games', ascending=False)
    
    # Bar plot showing the number of games played by each player
    fig1 = px.bar(
        summary_df_bar,
        x='player_name',
        y='Played_Games',
        color='player_name',
        color_discrete_map=player_color_map,
        title='Number of Games Played by Each Player',
        labels={'Played_Games': 'Number of Games', 'player_name': 'Player Name'},
        )
    
    fig1.update_layout(
    plot_bgcolor='white',
    showlegend=False,

)
    # Replace these example scatter plots with relevant data and logic
    fig2 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Statistics')
    
    # FIG 3 Pie Chart
    game_data_df_pie = game_data_df[game_data_df['win'] == 1]  # Filter for wins
    summary_df_pie = game_data_df_pie.groupby(['player_name']).agg(Games_won=('game_id', 'count')).reset_index()
    
    fig3 = px.pie(
    summary_df_pie,
    names='player_name',
    values='Games_won',
    color='player_name',
    color_discrete_map=player_color_map,
    title='Total Games Won',
)   
    
    fig3.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=True, 
    legend_title_text='Player Name'
)
    
    fig4 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Mana Value Distribution of all decks played')

    # Return the layout with graphs arranged in a 2x2 grid
    return html.Div([
        html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(2, 1fr)',
            'gap': '20px'
        })
    ])
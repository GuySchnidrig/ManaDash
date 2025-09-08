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

from backend.game_data import *


def create_landing_page(player_color_map, archetype_color_map):
    vintage_standings_df = get_vintage_standings()
    archetype_game_winrate = get_data('archetype_game_winrate')
    player_game_and_match_winrate = get_data('player_game_and_match_winrate')
    
    # Drafts plot
    # Create summary DataFrame for Drafts plot
    summary_df_bar = vintage_standings_df.groupby(['player']).agg(Played_Games=('draft_id', 'count')).reset_index()
    summary_df_bar = summary_df_bar.sort_values('Played_Games', ascending=False)
    
 
    draftbar = px.bar(
        summary_df_bar,
        x='player',
        y='Played_Games',
        color='player',
        color_discrete_map=player_color_map,
        title='Drafts Attended',
        labels={'Played_Games': 'Count', 'player': ''},
    )
    draftbar.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )

    # Archtypes plot
    # Create summary DataFrame for Drafts plot
    summary_df_bar = archetype_game_winrate
    summary_df_bar = summary_df_bar.sort_values('game_win_rate', ascending=False)

    archetype_fig = px.bar(
    summary_df_bar,
    x='archetype',
    y='game_win_rate',
    color='archetype',
    color_discrete_map=archetype_color_map,
    title='Archetype Game Win Rate',
    labels={'game_win_rate': 'Game Win Rate', 'archetype': ''},
    )
    
    archetype_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    archetype_fig.update_xaxes(
    tickangle=0,  # Can keep horizontal or slightly tilted
    ticktext=wrap_labels(summary_df_bar['archetype']),
    tickvals=summary_df_bar['archetype']
    )
    archetype_fig.update_yaxes(
    range=[0.3, summary_df_bar['game_win_rate'].max()],
    title='Game Win Rate'
)
    # Pie chart for games won
    game_data_df_pie = vintage_standings_df[vintage_standings_df['standing'] == 1]  # Filter for wins
    summary_df_pie = game_data_df_pie.groupby(['player']).agg(games_won=('draft_id', 'count')).reset_index()

    piewon = px.pie(
        summary_df_pie,
        names='player',
        values='games_won',
        color='player',
        color_discrete_map=player_color_map,  # use full mapping
        title='Drafts Won',
    )
    piewon.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True, 
        legend_title_text='Player Name'
    )
    
    # Gamewinrate 
    summary_df_avg_points = player_game_and_match_winrate
    # Sort 
    summary_df_avg_points = summary_df_avg_points.sort_values('game_win_rate', ascending=False)

    avg_points_fig = px.bar(
        summary_df_avg_points,
        x='player',
        y='game_win_rate',
        color='player',
        color_discrete_map=player_color_map,
        title='Game Win Rate',
        labels={'game_win_rate': 'Game Win Rate', 'player': ''}
    )

    avg_points_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False,
        yaxis=dict(title='Game Win Rate')
    )

    return dcc.Loading(
            id="loading-icon",
            type="circle",
            children=html.Div([
        dcc.Graph(figure=draftbar,
                          config={
                              'displayModeBar': False
                              }),  
        dcc.Graph(figure=archetype_fig,
                          config={
                              'displayModeBar': False
                              }),  
        dcc.Graph(figure=piewon,
                          config={
                              'displayModeBar': False
                              }),
        dcc.Graph(figure=avg_points_fig,
                          config={
                              'displayModeBar': False
                              }),
    ], className="responsive-grid", style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(2, 1fr)',  # 2 columns by default
        'gridTemplateRows': 'auto auto',          # Adjust rows to the content automatically
        'gap': '20px',
        # Add a media query to handle responsive design
        '@media (max-width: 768px)': {
            'gridTemplateColumns': '1fr'  # On small screens, stack items vertically
        }
    })
    )

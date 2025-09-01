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
from backend.game_data import *
def create_archetypes_page(player_color_map, archetype_color_map, decktype_color_map):
    
    vintage_decks_df = get_vintage_decks()
    decks_with_standings = get_decks_with_standings()
    
    archetype_game_winrate = get_data('archetype_game_winrate')
    decktype_game_winrate = get_data('decktype_game_winrate')

    archetype_match_winrate = get_data('archetype_match_winrate')
    decktype_match_winrate = get_data('decktype_match_winrate')

    # Archtypes plot
    summary_df_bar = decks_with_standings.groupby(['archetype']).agg(arche_types_count=('deck_id', 'nunique')).reset_index()
    summary_df_bar = summary_df_bar.sort_values('arche_types_count', ascending=False)

    archetype_fig = px.bar(
    summary_df_bar,
    x='archetype',
    y='arche_types_count',
    color='archetype',
    color_discrete_map=archetype_color_map,
    title='Archetypes',
    labels={'arche_types_count': 'Count', 'archetype': ''},
    )
    
    archetype_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    
    # Decktypes plot
    summary_df_bar = decks_with_standings.groupby(['decktype']).agg(deck_types_count=('deck_id', 'nunique')).reset_index()
    summary_df_bar = summary_df_bar.sort_values('deck_types_count', ascending=False).head(10)


    decktype_fig = px.bar(
    summary_df_bar,
    x='decktype',
    y='deck_types_count',
    color='decktype',
    color_discrete_map=decktype_color_map,
    title='Decktype',
    labels={'deck_types_count': 'Count', 'decktype': ''},
    )
    
    decktype_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    
    # Archtypes win plot
    summary_decks_with_standings = archetype_game_winrate.sort_values('game_win_rate', ascending=False)

    win_archetype_fig = px.bar(
    summary_decks_with_standings,
    x='archetype',
    y='game_win_rate',
    color='archetype',
    color_discrete_map=archetype_color_map,
    title='Winning Archetypes',
    labels={'game_win_rate': 'Game Win Rate', 'archetype': ''},
    )
    
    win_archetype_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    
    # Decktpyes win plot

    decktype_game_winrate_plot = decktype_game_winrate.sort_values('game_winrate', ascending=False).head(10)

    win_decktype_fig = px.bar(
    decktype_game_winrate_plot,
    x='decktype',
    y='game_winrate',
    color='decktype',
    color_discrete_map=decktype_color_map,
    title='Winning Decktypes',
    labels={'game_winrate': 'Game Win Rate', 'decktype': ''},
    )
    
    win_decktype_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    
    # Archtypes win plot match
    archetype_match_winrate_plot_df = archetype_match_winrate.sort_values('match_win_rate', ascending=False)

    archetype_match_winrate_plot = px.bar(
    archetype_match_winrate_plot_df,
    x='archetype',
    y='match_win_rate',
    color='archetype',
    color_discrete_map=archetype_color_map,
    title='Winning Archetypes',
    labels={'match_win_rate': 'Match Win Rate', 'archetype': ''},
    )
    
    archetype_match_winrate_plot.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    
    # Decktpyes win plot match

    summary_decks_with_standings_decktype = decktype_match_winrate.sort_values('match_win_rate', ascending=False).head(10)

    decktype_match_winrate_plot = px.bar(
    summary_decks_with_standings_decktype,
    x='decktype',
    y='match_win_rate',
    color='decktype',
    color_discrete_map=decktype_color_map,
    title='Winning Decktypes',
    labels={'match_win_rate': 'Match Win Rate', 'decktype': ''},
    )
    
    decktype_match_winrate_plot.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    

  # Return the layout with graphs and multiple tables arranged in a grid
    return html.Div([
            dcc.Graph(figure=archetype_fig,
                          config={
                              'displayModeBar': False  # This hides the mode bar
                              }),
            dcc.Graph(figure=decktype_fig,
                          config={
                              'displayModeBar': False  # This hides the mode bar
                              }),
            dcc.Graph(figure=win_archetype_fig,
                          config={
                              'displayModeBar': False  # This hides the mode bar
                              }),
            dcc.Graph(figure=win_decktype_fig,
                          config={
                              'displayModeBar': False  # This hides the mode bar
                              }),
            dcc.Graph(figure=archetype_match_winrate_plot,
                          config={
                              'displayModeBar': False  # This hides the mode bar
                              }),
            dcc.Graph(figure=decktype_match_winrate_plot,
                          config={
                              'displayModeBar': False  # This hides the mode bar
                              })
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
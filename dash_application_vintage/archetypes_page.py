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
from backend.game_data import get_vintage_standings
from backend.game_data import get_vintage_decks
from backend.game_data import get_decks_with_standings
def create_archetypes_page(player_color_map, archetype_color_map, decktype_color_map):
    
    vintage_decks_df = get_vintage_decks()
    decks_with_standings = get_decks_with_standings()
    
    # Archtypes plot
    summary_df_bar = vintage_decks_df.groupby(['archetype']).agg(arche_types_count=('deck_id', 'count')).reset_index()
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
    summary_df_bar = vintage_decks_df.groupby(['decktype']).agg(deck_types_count=('deck_id', 'count')).reset_index()
    summary_df_bar = summary_df_bar.sort_values('deck_types_count', ascending=False)

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
    decks_with_standings_filter = decks_with_standings[decks_with_standings['standing'] == 1]
    
    summary_decks_with_standings = decks_with_standings_filter.groupby(['archetype']).agg(arche_types_count=('deck_id', 'count')).reset_index()
    summary_decks_with_standings = summary_decks_with_standings.sort_values('arche_types_count', ascending=False)

    win_archetype_fig = px.bar(
    summary_decks_with_standings,
    x='archetype',
    y='arche_types_count',
    color='archetype',
    color_discrete_map=archetype_color_map,
    title='Winning Archetypes',
    labels={'arche_types_count': 'Wins', 'archetype': ''},
    )
    
    win_archetype_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    
    # Decktpyes win plot
    decks_with_standings_filter = decks_with_standings[decks_with_standings['standing'] == 1]
    summary_decks_with_standings_decktype = decks_with_standings_filter.groupby(['decktype']).agg(deck_types_count=('deck_id', 'count')).reset_index()
    summary_decks_with_standings_decktype = summary_decks_with_standings_decktype.sort_values('deck_types_count', ascending=False)

    win_decktype_fig = px.bar(
    summary_decks_with_standings_decktype,
    x='decktype',
    y='deck_types_count',
    color='decktype',
    color_discrete_map=decktype_color_map,
    title='Winning Decktypes',
    labels={'deck_types_count': 'Wins', 'decktype': ''},
    )
    
    win_decktype_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    
    # archtype win percentage plot
    summary_archetype_with_standings_percentage = (
    decks_with_standings
    .assign(is_win=lambda df: df['standing'] == 1)  # Add a boolean column for wins
    .groupby(['archetype'])
    .agg(total_games=('deck_id', 'count'), total_wins=('is_win', 'sum'))
    .reset_index())
    
    summary_archetype_with_standings_percentage['win_percentage'] = (summary_archetype_with_standings_percentage['total_wins'] / summary_archetype_with_standings_percentage['total_games']) * 100
    
    # Plot the win percentage for each and archetype
    win_archetype_percentage_fig = px.bar(
        summary_archetype_with_standings_percentage,
        x='archetype',
        y='win_percentage',
        color='archetype',
        color_discrete_map=archetype_color_map,
        title='Win Percentage of Archetypes',
        labels={'win_percentage': 'Win Percentage', 'archetype': ''}
    )

    win_archetype_percentage_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    
    
    # decktype win percentage plot
    summary_decks_with_standings_percentage = (
    decks_with_standings
    .assign(is_win=lambda df: df['standing'] == 1)  # Add a boolean column for wins
    .groupby(['decktype'])
    .agg(total_games=('deck_id', 'count'), total_wins=('is_win', 'sum'))
    .reset_index())
    
    summary_decks_with_standings_percentage['win_percentage'] = (summary_decks_with_standings_percentage['total_wins'] / summary_decks_with_standings_percentage['total_games']) * 100

    
        # Plot the win percentage for each decktype
    win_decktype_percentage_fig = px.bar(
        summary_decks_with_standings_percentage,
        x='decktype',
        y='win_percentage',
        color='decktype',
        color_discrete_map=decktype_color_map,
        title='Win Percentage of Decktypes',
        labels={'win_percentage': 'Win Percentage', 'decktype': ''}
    )

    win_decktype_percentage_fig.update_layout(
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
            dcc.Graph(figure=win_archetype_percentage_fig,
                          config={
                              'displayModeBar': False  # This hides the mode bar
                              }),
            dcc.Graph(figure=win_decktype_percentage_fig,
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
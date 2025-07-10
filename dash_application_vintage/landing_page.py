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

from backend.game_data import get_vintage_drafts
from backend.game_data import get_vintage_standings
from backend.game_data import get_vintage_decks
from backend.game_data import get_vintage_players

def create_landing_page(player_color_map, archetype_color_map):
    vintage_drafts_df = get_vintage_drafts()
    vintage_standings_df = get_vintage_standings()
    vintage_decks_df = get_vintage_decks()
    vintage_players_df = get_vintage_players()

    combined_df = pd.merge(vintage_standings_df, vintage_players_df, on='player_id', how='left')
    
    # Drafts plot
    # Create summary DataFrame for Drafts plot
    summary_df_bar = combined_df.groupby(['player_name']).agg(Played_Games=('draft_id', 'count')).reset_index()
    summary_df_bar = summary_df_bar.sort_values('Played_Games', ascending=False)
    
 
    draftbar = px.bar(
        summary_df_bar,
        x='player_name',
        y='Played_Games',
        color='player_name',
        color_discrete_map=player_color_map,
        title='Drafts',
        labels={'Played_Games': 'Count', 'player_name': ''},
    )
    draftbar.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )

    # Archtypes plot
    # Create summary DataFrame for Drafts plot
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
    


    # Pie chart for games won
    game_data_df_pie = combined_df[combined_df['standing'] == 1]  # Filter for wins
    summary_df_pie = game_data_df_pie.groupby(['player_name']).agg(Games_won=('draft_id', 'count')).reset_index()
    
    piewon = px.pie(
        summary_df_pie,
        names='player_name',
        values='Games_won',
        color='player_name',
        color_discrete_map=player_color_map,
        title='Drafts Won',
    )
    piewon.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True, 
        legend_title_text='Player Name'
    )
    
    # Points plot
    # Create summary DataFrame for Drafts plot
    summary_df_avg_points = combined_df.groupby('player_name').agg(
    avg_gamewins_per_draft=('game_wins', 'mean'),   # average game wins per draft
    Played_Games=('draft_id', 'count')         # total drafts played
    ).reset_index()
    # Optional: sort by average points descending
    summary_df_avg_points = summary_df_avg_points.sort_values('avg_gamewins_per_draft', ascending=False)

    avg_points_fig = px.bar(
        summary_df_avg_points,
        x='player_name',
        y='avg_gamewins_per_draft',
        color='player_name',
        color_discrete_map=player_color_map,
        title='Game Wins per Draft',
        labels={'avg_gamewins_per_draft': 'Average Points', 'player_name': ''}
    )

    avg_points_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False,
        yaxis=dict(title='Average Game Wins')
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

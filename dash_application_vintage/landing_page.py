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

def create_landing_page(player_color_map):
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
    color_discrete_map=player_color_map,
    title='Archetypes',
    labels={'arche_types_count': 'Count', 'archetype': ''},
    )
    
    archetype_fig.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    
    # Create summary DataFrame for the main summary table
    summary_table = {
        'Total Drafts': len(vintage_standings_df['draft_id'].unique()),
        'Unique Players': len(vintage_players_df['player_name'].unique()),
        'Unique Archetypes': len(vintage_decks_df['archetype'].unique()),
        'Unique Decktypes': len(vintage_decks_df['decktype'].unique())
    }
    summary_table = pd.DataFrame([summary_table])

    summary_table = dash_table.DataTable(
        id='summary-table',
        columns=[{'name': col, 'id': col} for col in summary_table.columns],
        data=summary_table.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data={
            'backgroundColor': 'white',
            'color': 'black'
        },
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

    # Return the layout with graphs and multiple tables arranged in a grid
    return html.Div([
        dcc.Graph(figure=draftbar),  
        dcc.Graph(figure=archetype_fig),  
        dcc.Graph(figure=piewon),
        html.Div(summary_table, style={'height': '400px', 'overflowY': 'auto'})
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
    

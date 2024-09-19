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


def create_landing_page(vintage_drafts_df, vintage_standings_df,vintage_players_df,vintage_decks_df, player_color_map):
    # Create summary DataFrame for bar plot
    summary_df_bar = vintage_standings_df.groupby(['player_id']).agg(Played_Games=('draft_id', 'count')).reset_index()
    summary_df_bar = summary_df_bar.sort_values('Played_Games', ascending=False)
    
    # Bar plot
    fig1 = px.bar(
        summary_df_bar,
        x='player_id',
        y='Played_Games',
        color='player_id',
        color_discrete_map=player_color_map,
        title='Number of Games Played by Each Player',
        labels={'Played_Games': 'Number of Games', 'player_id': 'Player Name'},
    )
    fig1.update_layout(
        plot_bgcolor='white',
        showlegend=False
    )
    
    # Create summary DataFrame for the main summary table
    summary_df_table = {
        'Total Drafts': len(vintage_standings_df['draft_id'].unique()),
        'Unique Players': len(vintage_players_df['player_name'].unique()),
        'Unique Archetypes': len(vintage_decks_df['archetype'].unique()),
        'Unique Decktypes': len(vintage_decks_df['decktype'].unique())
    }
    summary_df = pd.DataFrame([summary_df_table])
    
    # Create a Dash DataTable to display the summary
    summary_table = dash_table.DataTable(
        id='summary-table',
        columns=[{'name': col, 'id': col} for col in summary_df.columns],
        data=summary_df.to_dict('records'),
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
    game_data_df_pie = vintage_drafts_df[vintage_standings_df['standing'] == 1]  # Filter for wins
    summary_df_pie = game_data_df_pie.groupby(['player_id']).agg(Games_won=('draft_id', 'count')).reset_index()
    
    fig3 = px.pie(
        summary_df_pie,
        names='player_id',
        values='Games_won',
        color='player_id',
        color_discrete_map=player_color_map,
        title='Total Games Won',
    )
    fig3.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True, 
        legend_title_text='Player Name'
    )
    


    # Box plot for win turns by win type
    # Assuming vintage_decks_df is already defined and contains your data
    filtered_data = vintage_decks_df[~vintage_decks_df['archetype'].isna()]

    # Count occurrences of each archetype
    archetype_counts = filtered_data['archetype'].value_counts().reset_index()
    archetype_counts.columns = ['archetype', 'count']
    
    fig4 = px.box(
        archetype_counts,
        x='archetype',
        y='count',
        title='Count of Archetypes',
        color='archetype'
    )
    fig4.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        xaxis_title="",
        yaxis_title="Count"
    )

    # Return the layout with graphs and multiple tables arranged in a grid
    return html.Div([
        html.Div([
            dcc.Graph(figure=fig1),
            html.Div([
                html.Div(summary_table, style={'height': '400px', 'overflowY': 'auto'}),  # Adjust height as needed
            ], style={
                'display': 'grid',
                'gridTemplateColumns': '1fr',  # Single column layout for tables
                'gap': '20px'
            }),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(2, 1fr)',
            'gridTemplateRows': 'auto auto',  # Adjusts rows to the content automatically
            'gap': '20px'
        })
    ])

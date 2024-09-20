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
    # Create summary DataFrame for bar plot
    summary_df_bar = game_data_df.groupby(['player_name']).agg(Played_Games=('game_id', 'count')).reset_index()
    summary_df_bar = summary_df_bar.sort_values('Played_Games', ascending=False)
    
    # Bar plot
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
        showlegend=False
    )
    
    # Create summary DataFrame for the main summary table
    summary_df_table = {
        'Total Games': len(game_data_df['game_id'].unique()),
        'Unique Players': len(game_data_df['player_name'].unique()),
        'Unique Commanders': len(game_data_df['deck_name'].unique()),
        'Average Win Turn': round(game_data_df['win_turn'].mean(), 2)
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
    
    # Additional table based on the R code
    additional_summary_df = (game_data_df
                             .groupby('deck_name')
                             .agg(Games_played=('deck_name', 'size'),
                                  Wins=('win', 'sum'))
                             .reset_index()
                             .sort_values('Games_played', ascending=False)
                             .head(10))
    
        # Rename columns for the additional table
    additional_summary_df = additional_summary_df.rename(columns={
        'deck_name': 'Commander',
        'Wins': 'Wins',
        'Games_played': 'Games played'
    })
    
    additional_table = dash_table.DataTable(
        id='additional-summary-table',
        columns=[{'name': col, 'id': col} for col in additional_summary_df.columns],
        data=additional_summary_df.to_dict('records'),
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
    
    # Box plot for win turns by win type
    filtered_data_Win_Type = game_data_df[~game_data_df['win_type'].isna() & (game_data_df['win'] == 1)]
    fig4 = px.box(
        filtered_data_Win_Type,
        x='win_type',
        y='win_turn',
        color='win_type',
        title='Win Turn by Win Type'
    )
    fig4.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        xaxis_title="",
        yaxis_title="Win Turn"
    )

    # Return the layout with graphs and multiple tables arranged in a grid
    return html.Div([
            dcc.Graph(figure=fig1),
            html.Div([
                html.Div(summary_table, style={'height': '100px', 'overflowY': 'auto'}),  # Adjust height as needed
                html.Div(additional_table, style={'height': '300px', 'overflowY': 'auto'})  # Adjust height as needed
            ], style={
                'display': 'grid',
                'gridTemplateColumns': '1fr',  # Single column layout for tables
                'gap': '20px'
            }),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
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
    
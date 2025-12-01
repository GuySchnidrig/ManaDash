# cards_page.py
import dash
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from backend.game_data import *

def create_cards_page(player_color_map, archetype_color_map, decktype_color_map):
    cards_df = get_data('card_game_winrate_per_season')
    sorted_game_data_df = cards_df.sort_values(by='games_played', ascending=False)
    
    return html.Div([
        # -----------------------------
        # FILTER BAR (flex aligned)
        # -----------------------------
        html.Div([
            # Season Dropdown
            html.Div([
                html.Label("Season", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='season-dropdown',
                    options=[
                        {'label': f"Season{s}" if s != '-All' else 'Season-All', 'value': s}
                        for s in sorted(cards_df['season_id'].unique())
                    ],
                    value=sorted(cards_df['season_id'].unique())[0],
                    clearable=False,
                    style={'width': '200px'}
                ),
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'marginRight': '20px'
            }),
            
            # Card Search
            html.Div([
                html.Label("Search Card", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Input(
                    id='card-search-input',
                    type='text',
                    placeholder='Search card...',
                    debounce=True,
                    style={'width': '200px', 'padding': '5px'}
                )
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'marginRight': '20px'
            }),
            
            # Min Games Filter
            html.Div([
                html.Label("Min Games Played", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Input(
                    id='min-games-filter',
                    type='number',
                    placeholder='Min games',
                    min=0,
                    value=10,
                    style={'width': '150px', 'padding': '5px'}
                )
            ], style={
                'display': 'flex',
                'flexDirection': 'column'
            }),
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'alignItems': 'flex-end',
            'marginBottom': '20px',
            'padding': '15px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '5px'
        }),
        
        # -----------------------------
        # SCATTER PLOT
        # -----------------------------
        dcc.Graph(
            id='card-scatter-plot',
            style={'marginTop': '10px', 'marginBottom': '20px'}
        ),
        
        # -----------------------------
        # TOP PERFORMERS SECTION
        # -----------------------------
        html.Div([
            html.H4("Top Performing Cards", style={'marginBottom': '10px'}),
            html.Div(id='top-cards-section')
        ], style={'marginBottom': '30px'}),
        
        # -----------------------------
        # DATA TABLE
        # -----------------------------
        html.H4("Detailed Card Statistics", style={'marginBottom': '10px'}),
        dash_table.DataTable(
            id='card-stats-table',
            sort_action='native',
            filter_action='native',
            filter_options={'case': 'insensitive'},
            page_size=20,
            columns=[
                {'name': 'Season', 'id': 'season_id'},
                {'name': 'Card Name', 'id': 'card_name'},
                {'name': 'Games Won', 'id': 'games_won', 'type': 'numeric'},
                {'name': 'Games Played', 'id': 'games_played', 'type': 'numeric'},
                {'name': 'Game Win Rate', 'id': 'game_win_rate', 'type': 'numeric', 'format': {'specifier': '.2%'}}
            ],
            data=sorted_game_data_df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'minWidth': '100px',
                'maxWidth': '300px',
                'textAlign': 'left',
                'padding': '10px'
            },
            style_header={
                'backgroundColor': '#2c3e50',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'left'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f8f9fa'
                },
                {
                    'if': {
                        'filter_query': '{game_win_rate} > 0.55',
                        'column_id': 'game_win_rate'
                    },
                    'backgroundColor': '#d4edda',
                    'color': '#155724'
                },
                {
                    'if': {
                        'filter_query': '{game_win_rate} < 0.45',
                        'column_id': 'game_win_rate'
                    },
                    'backgroundColor': '#f8d7da',
                    'color': '#721c24'
                }
            ]
        )
    ])


def create_card_scatter_plot(filtered_df):
    """
    Enhanced scatter plot with better styling and information
    """
    fig = go.Figure()
    
    # Add scatter trace with custom hover template
    fig.add_trace(go.Scatter(
        x=filtered_df['games_played'],
        y=filtered_df['game_win_rate'],
        mode='markers',
        marker=dict(
            size=filtered_df['games_played'] / filtered_df['games_played'].max() * 30 + 5,
            color=filtered_df['game_win_rate'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Win Rate"),
            line=dict(width=1, color='white'),
            opacity=0.7
        ),
        text=filtered_df['card_name'],
        hovertemplate='<b>%{text}</b><br>' +
                      'Games Played: %{x}<br>' +
                      'Win Rate: %{y:.2%}<br>' +
                      '<extra></extra>'
    ))
    
    # Add 50% reference line
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray")
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Card Performance: Win Rate vs Games Played',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        xaxis_title='Games Played',
        yaxis_title='Game Win Rate',
        yaxis_tickformat='.0%',
        hovermode='closest',
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        height=600,
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            zeroline=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            range=[
                max(0, filtered_df['game_win_rate'].min() - 0.05),
                min(1, filtered_df['game_win_rate'].max() + 0.05)
            ]
        )
    )
    
    return fig


def create_summary_stats(filtered_df):
    """
    Create summary statistics cards
    """
    total_cards = len(filtered_df)
    avg_winrate = filtered_df['game_win_rate'].mean()
    total_games = filtered_df['games_played'].sum()
    high_performers = len(filtered_df[filtered_df['game_win_rate'] > 0.55])
    
    return html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Cards", className="card-title"),
                        html.H2(f"{total_cards}", style={'color': '#3498db'})
                    ])
                ], style={'textAlign': 'center'}),
                width=3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Average Win Rate", className="card-title"),
                        html.H2(f"{avg_winrate:.1%}", style={'color': '#2ecc71'})
                    ])
                ], style={'textAlign': 'center'}),
                width=3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Games", className="card-title"),
                        html.H2(f"{total_games:,}", style={'color': '#9b59b6'})
                    ])
                ], style={'textAlign': 'center'}),
                width=3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H5("High Performers (>55%)", className="card-title"),
                        html.H2(f"{high_performers}", style={'color': '#e74c3c'})
                    ])
                ], style={'textAlign': 'center'}),
                width=3
            ),
        ])
    ])


def create_top_cards_display(filtered_df, n=5):
    """
    Display top performing cards
    """
    # Filter for cards with significant sample size
    significant_cards = filtered_df[filtered_df['games_played'] >= 20]
    
    if len(significant_cards) == 0:
        return html.P("No cards with sufficient games played")
    
    top_cards = significant_cards.nlargest(n, 'game_win_rate')
    
    cards_list = []
    for idx, row in top_cards.iterrows():
        cards_list.append(
            html.Div([
                html.H6(row['card_name'], style={'marginBottom': '5px', 'color': '#2c3e50'}),
                html.P([
                    html.Span(f"{row['game_win_rate']:.1%}", 
                             style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#27ae60'}),
                    html.Span(f" ({row['games_played']} games)", 
                             style={'fontSize': '14px', 'color': '#7f8c8d'})
                ], style={'marginBottom': '0'})
            ], style={
                'padding': '15px',
                'backgroundColor': '#ecf0f1',
                'borderRadius': '5px',
                'marginBottom': '10px',
                'borderLeft': '4px solid #27ae60'
            })
        )
    
    return html.Div(cards_list)
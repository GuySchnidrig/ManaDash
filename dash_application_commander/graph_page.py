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

def create_graph_page():
    df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    })
    fig1 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Games Played')
    fig2 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Statistics')
    fig3 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Total Games Won')
    fig4 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Mana Value Distribution of all decks played')

    return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
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
    
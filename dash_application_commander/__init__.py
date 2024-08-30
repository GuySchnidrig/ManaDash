import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from backend.game_data import get_games

 
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

game_data_df = get_games()

def create_dash_application_commander(flask_app):
    dash_app = dash.Dash(server=flask_app, 
                         name="commander_dash", 
                         url_base_pathname="/commander/", 
                         suppress_callback_exceptions=True)

    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Commander", href="/commander/"),
                dbc.NavLink("Graphs", href="/commander/graphs"),
                dbc.NavLink("Game Data", href="/commander/game_data")
            ],
            brand=[
                html.Img(
                    src="https://raw.githubusercontent.com/GuySchnidrig/ManaDash/868018bbeeabbd486be438a99f62744b0ec9c7de/icons/scroll-unfurled-svgrepo-com.svg",
                    style={"width": "30px", "height": "30px"}
                ),
                html.Span("ManaDash", style={"margin-left": "8px"})
            ],
            brand_href="/",
            color="primary",
            dark=True,
            className="navbar"  
        ),
        html.Div(id='page-content')
    ])
    
    @dash_app.callback(
        dash.dependencies.Output('page-content', 'children'),
        [dash.dependencies.Input('url', 'pathname')]
    )
    
    def display_page(pathname):
        if pathname == '/commander/graphs':
            return Create_Graph_Page()
        elif pathname == '/commander/game_data':
            return Game_Data_page()
        elif pathname == '/':
            return dcc.Location(pathname='/redirect_to_flask', id='redirect_to_flask')
        else:
            return create_landing_page()
        

    return dash_app

def create_landing_page():
    
    fig1 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Games Played')
    fig2 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Statistics')
    fig3 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Total Games Won')
    fig4 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Mana Value Distribution of all decks played')

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
    
def Create_Graph_Page():
    fig1 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Games Played')
    fig2 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Statistics')
    fig3 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Total Games Won')
    fig4 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Mana Value Distribution of all decks played')

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
    
def Game_Data_page():
    return html.Div([
        # Data table
        
        dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in game_data_df.columns],
            data=game_data_df.to_dict('records'),
            style_table={'overflowX': 'auto'},  # Adds horizontal scroll if needed
            style_cell={
                'textAlign': 'left',
                'padding': '5px'
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )
    ])

    
    


    

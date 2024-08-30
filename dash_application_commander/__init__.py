import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from backend.game_data import get_games
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

 
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

# Get game data
game_data_df = get_games()

# Generate color mapping
unique_players = game_data_df['player_name'].unique()
palette = sns.color_palette("hls", len(unique_players), desat = 0.85)
color_list = [mcolors.to_hex(color) for color in palette]

player_color_map = dict(zip(unique_players, color_list))

# Dash APP
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
    # Create summary DataFrame
    summary_df_bar = game_data_df.groupby(['player_name']).agg(Played_Games=('game_id', 'count')).reset_index()
    summary_df_bar = summary_df_bar.sort_values('Played_Games', ascending=False)
    
    # Bar plot showing the number of games played by each player
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
    showlegend=False,

)
    # Replace these example scatter plots with relevant data and logic
    fig2 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Statistics')
    
    # FIG 3 Pie Chart
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
    
    fig4 = px.scatter(df, x='Fruit', y='Amount', color='City', title='Mana Value Distribution of all decks played')

    # Return the layout with graphs arranged in a 2x2 grid
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
    
    sorted_game_data_df = game_data_df.sort_values(by='game_id', ascending=False)
    columns_to_hide = {'uploader', 'color'}    
    visible_columns = [col for col in game_data_df.columns if col not in columns_to_hide]

    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in visible_columns],
            data=sorted_game_data_df[visible_columns].to_dict('records'),
            style_table={'overflowX': 'auto'},  
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

    
    


    

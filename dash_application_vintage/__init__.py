# Import libraries
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import seaborn as sns
import matplotlib.colors as mcolors

# Import local functions and pages
from backend.game_data import get_vintage_players

from dash_application_vintage.landing_page import create_landing_page
from dash_application_vintage.decks_page import create_decks_page
from dash_application_vintage.player_page import create_player_page

from dash_application_vintage.data_page import create_standings_page

# Get game data
vintage_players_df = get_vintage_players()

# Generate color mapping
unique_players = vintage_players_df['player_name'].unique()
palette = sns.color_palette("hls", len(unique_players), desat = 0.85)
color_list = [mcolors.to_hex(color) for color in palette]

player_color_map = dict(zip(unique_players, color_list))

# Dash APP
def create_dash_application_vintage(flask_app):
    dash_app = dash.Dash(server=flask_app, 
                         name="vintage_dash", 
                         url_base_pathname="/vintage/", 
                         suppress_callback_exceptions=True)

    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Vintage", href="/vintage/"),
                dbc.NavLink("Decks", href="/vintage/decks"),
                dbc.NavLink("Player", href="/vintage/player"),
                dbc.NavLink("Standings", href="/vintage/standings")
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
        if pathname == '/vintage/player':
            return create_player_page()
        elif pathname == '/vintage/decks':
            return create_decks_page()
        elif pathname == '/vintage/standings':
            return create_standings_page()
        elif pathname == '/':
            return dcc.Location(pathname='/redirect_to_flask', id='redirect_to_flask')
        else:
            return create_landing_page(player_color_map)

    return dash_app

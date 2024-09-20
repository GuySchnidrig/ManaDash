# Import libraries
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import seaborn as sns
import matplotlib.colors as mcolors

# Import local functions and pages
from backend.game_data import get_games

from dash_application_commander.landing_page import create_landing_page
from dash_application_commander.graph_page import create_graph_page
from dash_application_commander.data_page import create_game_data_page

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
    
        # Set custom index string with favicon, but include required Dash placeholders
    dash_app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
            <title>ManaDash</title>
            {%metas%}
            {%css%}
        </head>
        <body>
            <div id="react-entry-point">
                {%app_entry%}
            </div>
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

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
            return create_graph_page()
        elif pathname == '/commander/game_data':
            return create_game_data_page(game_data_df)
        elif pathname == '/':
            return dcc.Location(pathname='/redirect_to_flask', id='redirect_to_flask')
        else:
            return create_landing_page(game_data_df, player_color_map)

    return dash_app

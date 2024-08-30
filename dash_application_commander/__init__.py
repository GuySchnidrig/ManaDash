import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)


def create_dash_application_commander(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/commander/", suppress_callback_exceptions=True)

    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Commander", href="/commander/"),
                dbc.NavLink("Page 1", href="/commander/page1"),
                dbc.NavLink("Page 2", href="/commander/page2")
            ],
            brand=[
                html.Img(
                    src="https://raw.githubusercontent.com/GuySchnidrig/ManaDash/868018bbeeabbd486be438a99f62744b0ec9c7de/icons/scroll-unfurled-svgrepo-com.svg",
                    style={"width": "30px", "height": "30px"}
                ),
                html.Span("ManaDash", style={"margin-left": "8px"})
            ],
            brand_href="/commander/",
            color="primary",
            dark=True,
            className="navbar"  # You can add a custom class if needed for additional styling
        ),
        html.Div(id='page-content')
    ])

    return dash_app
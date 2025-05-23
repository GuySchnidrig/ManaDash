import dash
from dash import html
import requests
from collections import defaultdict
from dash.dependencies import Input, Output, State, ALL
from dash import callback_context

card_names = [
    "Gilded Goose",
    "Psychic Frog",
    "Sylvan Caryatid",
    "The Goose Mother",
    "Scavenging Ooze",
    "Springheart Nantuko",
    "Nadu, Winged Wisdom",
    "Spitting Dilophosaurus",
    "Unruly Krasis",
    "Tireless Tracker",
    "Leovold, Emissary of Trest",
    "Manglehorn",
    "Fallen Shinobi",
    "Mox Sapphire",
    "Tropical Island",
    "Misty Rainforest",
    "Bountiful Landscape",
    "Zuran Orb",
    "Mana Crypt",
    "Zagoth Triome",
    "Verdant Catacombs",
    "Dismember",
    "Inquisition of Kozilek",
    "Duress",
    "Skullclamp",
    "Brainstorm",
    "Mana Drain",
    "Daze",
    "Lightning Greaves",
    "Witherbloom Command",
    "Bitter Triumph",
    "Force of Negation",
    "Timetwister",
    "Narset, Parter of Veils",
    "Virtue of Persistence"
]

def fetch_card_data(name):
    url = f"https://api.scryfall.com/cards/named?fuzzy={name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"],
            "image_url": data["image_uris"]["normal"],
            "cmc": data["cmc"],
            "is_creature": "creature" in [t.lower() for t in data["type_line"].split(" ")],
        }
    return None

cards = [fetch_card_data(name) for name in card_names]
cards = [card for card in cards if card is not None]

def group_by_cmc(card_list, all_cmcs):
    cmc_groups = defaultdict(list)
    for card in card_list:
        cmc_groups[card["cmc"]].append(card)
    # Ensure all cmcs appear even if empty
    return {cmc: cmc_groups.get(cmc, []) for cmc in sorted(all_cmcs)}

# Separate creatures and non-creatures
creature_cards = [c for c in cards if c["is_creature"]]
non_creature_cards = [c for c in cards if not c["is_creature"]]

# Get the union of all CMCs
all_cmcs = sorted(set(c["cmc"] for c in creature_cards + non_creature_cards))

# Group with normalized CMCs
creatures = group_by_cmc(creature_cards, all_cmcs)
non_creatures = group_by_cmc(non_creature_cards, all_cmcs)

app = dash.Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>MTG Cards Viewer</title>
        {%favicon%}
        {%css%}
        <style>
            body, html {
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: Arial, sans-serif;
            }
            .main-container {
                display: flex;
                gap: 20px;
                padding: 20px;
            }
            .cards-container {
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 40px;
            }
            .row-container {
                display: flex;
                gap: 20px;
            }
            .cmc-stack {
                display: flex;
                flex-direction: column;
                align-items: center;
                position: relative;
                width: 240px;  /* fixed width for equal columns */
                min-height: 340px; /* ensure some height so empty columns show */
                /* border: 1px solid #ddd; /* optional, to visualize columns */
                padding-top: 30px;
                box-sizing: border-box;
            }
            .card {
                transition: transform 0.2s ease;
                transform-origin: center center;
                width: 223px;
                height: 310px;
                margin-top: -270px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
                z-index: 1;
                cursor: pointer;
            }
            .card:first-child {
                margin-top: 0;
            }
            /* Removed hover zoom effect */
            /*
            .card:hover {
                transform: scale(1.5);
                z-index: 10;
                position: relative;
            }
            */
            .cmc-label {
                margin-bottom: 8px;
                font-weight: bold;
                font-size: 16px;
                text-align: center;
            }
            .stats-panel {
                width: 300px;
                padding: 20px;
                background-color: #f9f9f9;
                border-left: 1px solid #ccc;
                font-size: 14px;
            }
            .stats-panel h3 {
                margin-top: 0;
                font-weight: bold;
                border-bottom: 1px solid #ccc;
                padding-bottom: 8px;
            }
            .stats-item {
                margin-bottom: 10px;
            }
            #zoomed-card-container {
                margin-top: 20px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

def render_row(grouped_cards):
    return html.Div([
        html.Div([
            html.Div([
                # html.Div(f"CMC: {cmc}", className="cmc-label"),
                html.Div([
                    html.Img(
                        src=card["image_url"], 
                        title=card["name"], 
                        className="card",
                        id={"type": "card-image", "index": card["name"]},
                        n_clicks=0,
                    )
                    for card in card_stack
                ])
            ], className="cmc-stack")
            for cmc, card_stack in grouped_cards.items()
        ], className="row-container")
    ])

def calculate_stats(cards):
    total_cards = len(cards)
    if total_cards == 0:
        avg_cmc = 0
    else:
        avg_cmc = sum(card["cmc"] for card in cards) / total_cards
    
    creatures = sum(1 for c in cards if c["is_creature"])
    non_creatures = total_cards - creatures
    
    return {
        "Total Cards": total_cards,
        "Average CMC": f"{avg_cmc:.2f}",
        "Creatures": creatures,
        "Non-Creatures": non_creatures,
    }

def render_stats_panel():
    all_cards = creature_cards + non_creature_cards
    stats = calculate_stats(all_cards)
    return html.Div([
        html.H3("Statistics"),
        *[html.Div(f"{key}: {value}", className="stats-item") for key, value in stats.items()]
    ], className="stats-panel")

app.layout = html.Div([
    html.H1("MTG Cards Stacked by CMC"),
    html.Div([
        html.Div([
            render_row(creatures),
            render_row(non_creatures),
        ], className="cards-container"),
        html.Div([
            render_stats_panel(),
            html.Div(id="zoomed-card-container")  # Zoomed card display below stats
        ], style={"display": "flex", "flexDirection": "column"})
    ], className="main-container")
])

@app.callback(
    Output("zoomed-card-container", "children"),
    Input({"type": "card-image", "index": ALL}, "n_clicks"),
    State({"type": "card-image", "index": ALL}, "id")
)
def display_zoomed_card(n_clicks_list, ids):
    ctx = callback_context

    if not ctx.triggered:
        return "Click a card above to zoom"

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # triggered_id will be a string representation of the dict, e.g. '{"index":"Gilded Goose","type":"card-image"}'
    import json
    triggered_id_dict = json.loads(triggered_id)

    card_name = triggered_id_dict["index"]
    card = next((c for c in cards if c["name"] == card_name), None)
    if not card:
        return "Card data not found."

    return html.Div([
        html.H4(card["name"]),
        html.Img(
            src=card["image_url"], 
            style={"width": "400px", "height": "auto", "boxShadow": "0 4px 12px rgba(0,0,0,0.3)"}
        ),
    ])

if __name__ == "__main__":
    app.run_server(debug=True)

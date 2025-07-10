import sqlite3
import pandas as pd
import os
import requests
from dash import callback_context, Input, Output, State, ALL, html
import dash_bootstrap_components as dbc
from collections import defaultdict
import json

# Define the path to your SQLite database relative to the root of your project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one directory
DB_PATH = os.path.join(ROOT_DIR, 'data', 'cmdr_tracker_v2.db')

DB_PATH_vintage = os.path.join(ROOT_DIR, 'data', 'vintage_cube.db')

def get_games():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = "SELECT * FROM game_data"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df


def get_vintage_drafts():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = "SELECT * FROM drafts"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df

def get_vintage_standings():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = "SELECT * FROM draft_standing"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df

def get_vintage_decks():
    try:
        with sqlite3.connect(DB_PATH_vintage) as db:
            query = """
            SELECT d.*, s.player_id AS player_id
            FROM decks d
            LEFT JOIN draft_standing s
                ON d.deck_id = s.deck_id
            """
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()
    return df


def get_vintage_players():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df

def get_decks_with_standings():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = """
                SELECT drafts.date,
                       decks.deck_id, archetype, decktype, draft_standing.draft_standing_id, 
                       draft_standing.draft_id, draft_standing.player_id, 
                       draft_standing.standing, draft_standing.points, 
                       draft_standing.omp, draft_standing.gwp, draft_standing.ogp
                FROM decks
                JOIN draft_standing ON decks.deck_id = draft_standing.deck_id
                JOIN drafts ON draft_standing.draft_id = drafts.draft_id

            """
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df

def get_player_elo():
    try:
        with sqlite3.connect(DB_PATH_vintage) as db:
            query = """
                SELECT pe.id,
                       pe.player_id,
                       p.player_name,
                       pe.draft_id,
                       pe.elo
                FROM player_elo pe
                LEFT JOIN Players p ON pe.player_id = p.player_id
            """
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()

    return df

def get_full_game_stats_table():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = """
                SELECT drafts.date,
                       drafts.season_id,
                       players.player_name,  
                       players.player_id,
                       archetype, decktype, 
                       draft_standing.draft_id,draft_standing.standing, 
                       draft_standing.points, draft_standing.omp, 
                       draft_standing.gwp, draft_standing.ogp
                       
                FROM decks
                JOIN draft_standing ON decks.deck_id = draft_standing.deck_id
                JOIN players ON draft_standing.player_id = players.player_id
                JOIN drafts ON draft_standing.draft_id = drafts.draft_id
            """
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df

def get_all_cards():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH_vintage) as db:
            # Use pandas to execute the SQL query and load data into a DataFrame
            query = """
                SELECT cards.card_id,
                       cards.card_name,
                       cards.cube_color_tag
                FROM cards
            """
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame on error

    return df

def fetch_card_data(name):
    url = f"https://api.scryfall.com/cards/named?fuzzy={name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"],
            "image_url": data["image_uris"]["normal"] if "image_uris" in data else "",
            "cmc": data["cmc"],
            "is_creature": "creature" in data["type_line"].lower(),
        }
    return None

def get_deck_card_names(player_id, deck_id):
    # Assuming vintage_decks_df has a list of cards per deck, or query your DB here
    # Example placeholder, you should replace with your actual card retrieval logic
    # For demo, return some static cards or query from your DB
    return [    "Gilded Goose",
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
    "Virtue of Persistence"]


def group_by_cmc(card_list):
    cmc_groups = defaultdict(list)
    for card in card_list:
        cmc_groups[card["cmc"]].append(card)

    # Sort the cards inside each group by name (or another attribute)
    for cmc in cmc_groups:
        cmc_groups[cmc].sort(key=lambda c: c["name"])

    # Sort the groups by cmc key (ascending)
    return dict(sorted(cmc_groups.items()))

def render_row(grouped_cards):
    rows = []
    overlap_px = 273
    card_width = '270px'
    column_style = {
    "width": card_width,
    "maxWidth": card_width,
    "flex": "0 0 auto"
    }
    
    # Prepare the 6 cmc keys explicitly: 0,1,2,3,4 and 5+ (5 or more)
    cmc_keys = [0, 1, 2, 3, 4, '5+']
    
    # Group all cards with CMC >= 5 into '5+'
    cards_5_plus = []
    for cmc, cards in list(grouped_cards.items()):
        if isinstance(cmc, (int, float)) and cmc >= 5:
            cards_5_plus.extend(cards)
            grouped_cards.pop(cmc, None)  # Remove from original
    
    grouped_cards['5+'] = cards_5_plus
    
    for cmc in cmc_keys:
        cards = grouped_cards.get(cmc, [])
        card_imgs = []
        total_cards = len(cards)
        for i, card in enumerate(cards):
            margin_top = 0 if i == 0 else -overlap_px
            card_imgs.append(
                html.Img(
                    src=card["image_url"],
                    title=card["name"],
                    id={"type": "card-image", "index": card["name"]},
                    n_clicks=0,
                    style={
                        "width": "100%",
                        "maxWidth": "223px",
                        "height": "310px",
                        "marginTop": f"{margin_top}px",
                        "position": "relative",
                        "zIndex": i + 1,
                        "border-radius": "12px",
                        "box-shadow": "0 4px 8px rgba(0,0,0,0.2)",
                        "border": "1px solid #ccc",
                        "object-fit": "cover",
                        "overflow": "visible",
                        "transition": "transform 0.2s, box-shadow 0.2s",
                        "cursor": "pointer",
                    }
                )
            )
        
        container_height = 310 + (total_cards - 1) * (310 - overlap_px) if total_cards > 0 else 310
        
        col_content = html.Div(
            card_imgs,
            style={
                "position": "relative",
                "minHeight": f"{container_height}px",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
            }
        )
        # Add a label for the CMC at the top of each column for clarity
        col_content = html.Div([
            col_content
        ])
        
        rows.append(dbc.Col(col_content, style=column_style))
    
    return dbc.Row(rows, className="gx-2 gy-4")



def calculate_stats(cards):
    total = len(cards)
    avg = sum(c["cmc"] for c in cards) / total if total else 0
    creatures = sum(1 for c in cards if c["is_creature"])
    return {
        "Total Cards": total,
        "Average CMC": f"{avg:.2f}",
        "Creatures": creatures,
        "Non-Creatures": total - creatures
    }

def render_stats_panel(stats):
    return html.Div([
        *[html.P(f"{key}: {val}") for key, val in stats.items()]
    ], className="border rounded p-3 bg-light")

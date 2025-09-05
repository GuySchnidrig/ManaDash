import pandas as pd
import os
import requests
from dash import callback_context, Input, Output, State, ALL, html
import dash_bootstrap_components as dbc
from collections import defaultdict
import json
import sqlite3
import re
from dash import dash_table

# Define the path to your CSV data directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one directory
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DB_PATH = os.path.join(ROOT_DIR, 'data', 'cmdr_tracker_v2.db')

# Global variable to store loaded data
_loaded_data = {}

def load_all_csv_data():
    """Load all CSV files from the data directory into memory at startup"""
    global _loaded_data
    
    if not os.path.exists(DATA_DIR):
        print(f"Data directory not found: {DATA_DIR}")
        return
    
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in {DATA_DIR}")
        return
    
    print(f"Found {len(csv_files)} CSV files in {DATA_DIR}")
    
    for csv_file in csv_files:
        file_path = os.path.join(DATA_DIR, csv_file)
        key = csv_file.replace('.csv', '')
        try:
            _loaded_data[key] = pd.read_csv(file_path)
            print(f"Loaded {csv_file} ({len(_loaded_data[key])} rows)")
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
            _loaded_data[key] = pd.DataFrame()

def get_data(table_name):
    """Get data for a specific table"""
    return _loaded_data.get(table_name, pd.DataFrame())

# Commander DB
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

# Vintage
def get_vintage_drafts():
    """Get drafts data"""
    return get_data('drafts')

def get_vintage_standings():
    """Get standings data"""
    return get_data('standings')

def get_vintage_decks():
    """Get decks with player info merged"""
    decks_df = get_data('drafted_decks')

    # Merge decks with standings to get player info
    merged = decks_df.merge(
        decks_df[['draft_id', 'player', 'season_id']],
        on=['draft_id', 'player', 'season_id'],
        how='left'
    )
    return merged

def get_vintage_players():
    """Get unique players from drafted_decks"""
    decks_df = get_data('standings')
    if decks_df.empty:
        return pd.DataFrame()
    
    # Extract unique players
    players = decks_df[['player', 'player_id']].drop_duplicates().reset_index(drop=True)

    return players

def get_decks_with_standings():
    """Get decks merged with standings and draft info"""
    decks_df = get_data('drafted_decks')
    standings_df = get_data('standings')
    drafts_df = get_data('drafts')
    
    if decks_df.empty or standings_df.empty or drafts_df.empty:
        return pd.DataFrame()
    
    # Merge all three tables
    merged = decks_df.merge(
        standings_df,
        on=['draft_id', 'player', 'player_id', 'season_id'],
        how='inner'
    ).merge(
        drafts_df[['draft_id','season_id', 'timestamp']],
        on='draft_id',
        how='left'
    )
    
    # Rename timestamp to date for consistency
    if 'timestamp' in merged.columns:
        merged = merged.rename(columns={'timestamp': 'date'})
    
    return merged

def get_player_elo():
    """ELO data"""
    player_elo = get_data('elo_development')
    return player_elo

def get_full_game_stats_table():
    """Get comprehensive player stats with draft info"""
    decks_df = get_data('drafted_decks')
    standings_df = get_data('standings')
    drafts_df = get_data('drafts')
    
    if decks_df.empty or standings_df.empty or drafts_df.empty:
        return pd.DataFrame()
    
    # Merge all tables
    merged = decks_df.merge(
        standings_df,
        on=['draft_id', 'player','player_id', 'season_id'],
        how='inner'
    ).merge(
        drafts_df[['draft_id', 'timestamp']],
        on='draft_id',
        how='left'
    )
    
    return merged

def get_all_cards():
    """Get unique cards from drafted_decks"""
    decks_df = get_data('drafted_decks')
    if decks_df.empty:
        return pd.DataFrame()
    
    # Extract unique cards
    if 'scryfallId' in decks_df.columns and 'cardName' in decks_df.columns:
        cards = decks_df[['scryfallId', 'cardName']].drop_duplicates()
        cards = cards.rename(columns={
            'scryfallId': 'card_id',
            'cardName': 'card_name'
        })
        # Add placeholder cube_color_tag if needed
        cards['cube_color_tag'] = ''  # You'd need to populate this based on your data
        return cards
    else:
        return pd.DataFrame(columns=['card_id', 'card_name', 'cube_color_tag'])

def fetch_card_data(name):
    """Fetch card data from Scryfall API and return first available image URL."""
    url = f"https://api.scryfall.com/cards/named?fuzzy={name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Default empty image URL
        image_url = ""

        # Case 1: single-faced card
        if "image_uris" in data:
            image_url = data["image_uris"].get("normal", "")
        # Case 2: double-faced or multi-faced card
        elif "card_faces" in data and len(data["card_faces"]) > 0:
            # Take the first face's normal image
            first_face = data["card_faces"][0]
            if "image_uris" in first_face:
                image_url = first_face["image_uris"].get("normal", "")

        return {
            "name": data["name"],
            "image_url": image_url,
            "cmc": data.get("cmc", 0),
            "is_creature": "creature" in data.get("type_line", "").lower(),
            "is_land": "land" in data.get("type_line", "").lower(),
        }

    return None

def get_deck_card_names(player_id, deck_id, draft_id):
    """
    Get all card names for a specific deck (by player + deck_id)
    from drafted_decks table.
    """
    decks_df = get_data('drafted_decks')

    # Filter by deck_id and player_id (if both exist in schema)
    filtered = decks_df[
        (decks_df['deck_id'] == deck_id) & 
        (decks_df['player_id'] == player_id) &
        (decks_df['draft_id'] == draft_id)
    ]

    # Assuming each row has a "cardName" column
    return filtered['card_name'].dropna().tolist()


def group_by_cmc(card_list):
    """Group cards by CMC"""
    cmc_groups = defaultdict(list)
    for card in card_list:
        cmc_groups[card["cmc"]].append(card)

    # Sort the cards inside each group by name
    for cmc in cmc_groups:
        cmc_groups[cmc].sort(key=lambda c: c["name"])

    # Sort the groups by cmc key (ascending)
    return dict(sorted(cmc_groups.items()))

def render_row(grouped_cards):
    """Render cards grouped by CMC"""
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
        
        col_content = html.Div([col_content])
        rows.append(dbc.Col(col_content, style=column_style))
    
    return dbc.Row(rows, className="gx-2 gy-4")

def calculate_stats(cards, player_id=None, deck_id=None, decks_df=None):
    """Calculate deck statistics excluding lands and optionally include deck metadata"""
    standings = get_vintage_standings()
    # Filter out lands
    non_land_cards = [c for c in cards if not c.get("is_land", False)]
   
    total = len(non_land_cards)
    avg = sum(c["cmc"] for c in non_land_cards) / total if total else 0
    creatures = sum(1 for c in non_land_cards if c.get("is_creature", False))
   
    # Initialize stats with placeholders for metadata
    stats = {
        "Archetype": "",
        "Deck Type": "",
        "Deck Color": "",
        "Average CMC": f"{avg:.2f}",
        "Creatures": creatures,
        "Non-Creatures": total - creatures,
        "Match Points": ""
    }
    
    # Add deck metadata if decks_df is provided
    if decks_df is not None and player_id is not None and deck_id is not None:
        deck_info = decks_df[
            (decks_df['player_id'] == player_id) &
            (decks_df['deck_id'] == deck_id)
        ]
        if not deck_info.empty:
            row = deck_info.iloc[0]
            stats["Archetype"] = row.get('archetype', '')
            stats["Deck Type"] = row.get('decktype', '')
            stats["Deck Color"] = row.get('deck_color_short', '')
            
            # Get draft_id from decks dataframe
            draft_id = row.get('draft_id')
            
            # Filter standings based on draft_id and player_id
            if draft_id is not None:
                filtered_standings = standings[
                    (standings['draft_id'] == draft_id) &
                    (standings['player_id'] == player_id)
                ]
                
                # Get match_points from filtered standings
                if not filtered_standings.empty:
                    standing_row = filtered_standings.iloc[0]
                    stats["Match Points"] = standing_row.get('match_points', 0)
   
    return stats


def render_stats_panel(stats):
    """Render statistics panel as horizontal table with better styling and no cutoff"""
    stats_df = pd.DataFrame([stats])
   
    return dash_table.DataTable(
        columns=[{"name": col, "id": col, "presentation": "markdown"} for col in stats_df.columns],
        data=stats_df.to_dict('records'),
        style_table={
            'overflowX': 'auto',     # allow horizontal scroll
            'width': '100%',          # table fills container
            'minWidth': '1000px',     # increased minimum width for more columns
            'margin': '10px 0'
        },
        style_cell={
            'textAlign': 'center',
            'padding': '4px 8px',     # reduced padding to fit more content
            'minWidth': '100px',      # reduced minimum column width
            'maxWidth': '150px',      # add maximum width to prevent excessive expansion
            'whiteSpace': 'normal',
            'height': 'auto',
            'fontFamily': 'Arial, sans-serif',
            'fontSize': '12px',       # slightly smaller font
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'
        },
        style_header={
            'backgroundColor': '#f0f0f0',
            'fontWeight': 'bold',
            'fontSize': '14px',
            'borderBottom': '2px solid #ccc'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 0},
                'backgroundColor': '#fafafa'
            }
        ],
        fixed_rows={'headers': True},
    )
    
# Initialize data loading - call this when your app starts
def initialize_data():
    """Call this function when your Dash app starts"""
    load_all_csv_data()
    
def wrap_labels(labels, max_len=12):
    wrapped_labels = []
    for label in labels:
        # Split at space, hyphen, or closing parenthesis, keep delimiters
        parts = re.split(r'(\s+|-|\))', label)
        line = ""
        lines = []
        for part in parts:
            # If adding this part exceeds max length, start a new line
            if len(line + part) > max_len:
                if line:
                    lines.append(line.strip())
                line = part
            else:
                line += part
        if line:
            lines.append(line.strip())
        wrapped_labels.append('<br>'.join(lines))
    return wrapped_labels
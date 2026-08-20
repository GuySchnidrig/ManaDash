import pandas as pd
import os
import requests
from collections import defaultdict
import sqlite3
import re
import seaborn as sns
import matplotlib.colors as mcolors

# Define the path to your data directory
# This file lives at src/backend/game_data.py, so go up two levels to reach repo root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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


def get_games():
    """Commander game data (unused now that commander is dropped, kept for reference)"""
    try:
        with sqlite3.connect(DB_PATH) as db:
            query = "SELECT * FROM game_data"
            df = pd.read_sql_query(query, db)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        df = pd.DataFrame()

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

    merged = decks_df.merge(
        decks_df[['draft_id', 'player', 'season_id']],
        on=['draft_id', 'player', 'season_id'],
        how='left'
    )
    return merged


def get_vs_player_game_and_match_winrate():
    """Head-to-head win rate data"""
    return get_data('vs_player_game_and_match_winrate')


def get_most_played_card_by_player():
    """Most played card per player"""
    return get_data('most_played_card_by_player')


def get_player_archetype_winrates():
    """Player win rates by archetype"""
    return get_data('player_archetype_winrates')


def get_player_decktype_winrates():
    """Player win rates by decktype"""
    return get_data('player_decktype_winrates')


def get_combined_winrates_per_season():
    """Combined card win rates per season"""
    return get_data('combined_winrates_per_season')


def get_vintage_players():
    """Get unique players from standings"""
    decks_df = get_data('standings')
    if decks_df.empty:
        return pd.DataFrame()

    players = decks_df[['player', 'player_id']].drop_duplicates().reset_index(drop=True)
    return players


def get_decks_with_standings():
    """Get decks merged with standings and draft info"""
    decks_df = get_data('drafted_decks')
    standings_df = get_data('standings')
    drafts_df = get_data('drafts')

    if decks_df.empty or standings_df.empty or drafts_df.empty:
        return pd.DataFrame()

    merged = decks_df.merge(
        standings_df,
        on=['draft_id', 'player', 'player_id', 'season_id'],
        how='inner'
    ).merge(
        drafts_df[['draft_id', 'season_id', 'timestamp']],
        on='draft_id',
        how='left'
    )

    if 'timestamp' in merged.columns:
        merged = merged.rename(columns={'timestamp': 'date'})

    return merged


def get_player_elo():
    """ELO data"""
    return get_data('elo_development')


def get_full_game_stats_table():
    """Get comprehensive player stats with draft info"""
    decks_df = get_data('drafted_decks')
    standings_df = get_data('standings')
    drafts_df = get_data('drafts')

    if decks_df.empty or standings_df.empty or drafts_df.empty:
        return pd.DataFrame()

    merged = decks_df.merge(
        standings_df,
        on=['draft_id', 'player', 'player_id', 'season_id'],
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

    if 'scryfallId' in decks_df.columns and 'cardName' in decks_df.columns:
        cards = decks_df[['scryfallId', 'cardName']].drop_duplicates()
        cards = cards.rename(columns={
            'scryfallId': 'card_id',
            'cardName': 'card_name'
        })
        cards['cube_color_tag'] = ''
        return cards
    else:
        return pd.DataFrame(columns=['card_id', 'card_name', 'cube_color_tag'])


def fetch_card_data(name):
    """Fetch card data from Scryfall API and return first available image URL."""
    url = f"https://api.scryfall.com/cards/named?fuzzy={name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        image_url = ""

        if "image_uris" in data:
            image_url = data["image_uris"].get("normal", "")
        elif "card_faces" in data and len(data["card_faces"]) > 0:
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
    Get all card names for a specific deck (by player + deck_id + draft_id)
    from drafted_decks table.
    """
    decks_df = get_data('drafted_decks')

    filtered = decks_df[
        (decks_df['deck_id'] == deck_id) &
        (decks_df['player_id'] == player_id) &
        (decks_df['draft_id'] == draft_id)
    ]

    return filtered['card_name'].dropna().tolist()


def group_cards_by_cmc(card_list):
    """
    Group cards by CMC, bucketing everything CMC >= 5 into a '5+' group.
    Returns a plain dict keyed by '0','1','2','3','4','5+' -> list of card dicts,
    JSON-serializable as-is (e.g. for export to a static site's data file).

    This replaces the old group_by_cmc + render_row combo: the CMC-bucketing
    logic is unchanged, but instead of returning Dash components it returns
    data. Rendering the actual card grid is now a front-end (OJS/HTML) concern.
    """
    cmc_groups = defaultdict(list)
    for card in card_list:
        cmc_groups[card["cmc"]].append(card)

    for cmc in cmc_groups:
        cmc_groups[cmc].sort(key=lambda c: c["name"])

    cmc_keys = [0, 1, 2, 3, 4, '5+']

    cards_5_plus = []
    for cmc, cards in list(cmc_groups.items()):
        if isinstance(cmc, (int, float)) and cmc >= 5:
            cards_5_plus.extend(cards)
            cmc_groups.pop(cmc, None)

    cmc_groups['5+'] = cards_5_plus

    # stringify keys so this is directly JSON-dumpable
    return {str(k): cmc_groups.get(k, []) for k in cmc_keys}


def calculate_stats(cards, player_id=None, deck_id=None, decks_df=None):
    """Calculate deck statistics excluding lands and optionally include deck metadata.
    Returns a plain dict - unchanged from the original, this was already
    Dash-free."""
    standings = get_vintage_standings()
    non_land_cards = [c for c in cards if not c.get("is_land", False)]

    total = len(non_land_cards)
    avg = sum(c["cmc"] for c in non_land_cards) / total if total else 0
    creatures = sum(1 for c in non_land_cards if c.get("is_creature", False))

    stats = {
        "Archetype": "",
        "Deck Type": "",
        "Deck Color": "",
        "Average CMC": f"{avg:.2f}",
        "Creatures": creatures,
        "Non-Creatures": total - creatures,
        "Match Points": ""
    }

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

            draft_id = row.get('draft_id')

            if draft_id is not None:
                filtered_standings = standings[
                    (standings['draft_id'] == draft_id) &
                    (standings['player_id'] == player_id)
                ]

                if not filtered_standings.empty:
                    standing_row = filtered_standings.iloc[0]
                    stats["Match Points"] = standing_row.get('match_points', 0)

    return stats


def initialize_data():
    """Call this once at build time (e.g. top of a shared Quarto setup chunk)"""
    load_all_csv_data()


def _make_color_map(series):
    """Build a {value: hex_color} map from a pandas Series using an HLS palette."""
    unique_vals = series.dropna().unique()
    palette = sns.color_palette("hls", len(unique_vals), desat=0.85)
    hex_colors = [mcolors.to_hex(c) for c in palette]
    return dict(zip(unique_vals, hex_colors))


def get_color_maps():
    """
    Build player/archetype/decktype color maps from the loaded data.
    Call this AFTER initialize_data(), so vintage_players_df/vintage_decks_df
    are populated. Returns a tuple: (player_color_map, archetype_color_map, decktype_color_map)

    Usage in a .qmd setup chunk:
        initialize_data()
        player_color_map, archetype_color_map, decktype_color_map = get_color_maps()
    """
    vintage_players_df = get_vintage_players()
    vintage_decks_df = get_vintage_decks()

    player_color_map = _make_color_map(vintage_players_df['player'])
    archetype_color_map = _make_color_map(vintage_decks_df['archetype'])
    decktype_color_map = _make_color_map(vintage_decks_df['decktype'])

    return player_color_map, archetype_color_map, decktype_color_map


def wrap_labels(labels, max_len=12):
    wrapped_labels = []
    for label in labels:
        parts = re.split(r'(\s+|-|\))', label)
        line = ""
        lines = []
        for part in parts:
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


def add_season_draft_labels(df, season_col='season_id', draft_col='draft_id'):
    """
    Adds numeric season, draft count within season, and season-draft labels to a dataframe.
    """
    df = df.copy()

    df['season_num'] = df[season_col].astype(str).str.extract(r'(\d+)').astype(int)

    unique_drafts = (
        df[['season_num', draft_col]]
        .drop_duplicates()
        .sort_values(['season_num', draft_col])
        .reset_index(drop=True)
    )

    unique_drafts['d_in_season'] = unique_drafts.groupby('season_num').cumcount() + 1

    df = df.merge(
        unique_drafts[['season_num', draft_col, 'd_in_season']],
        on=['season_num', draft_col],
        how='left'
    )

    df['season_draft_label'] = df.apply(
        lambda row: f"S{row['season_num']}D{row['d_in_season']}", axis=1
    )

    return df

def initialize_quarto_data():
    """
    Initialize Plotly and load all shared data used by Quarto dashboards.

    Returns
    -------
    dict
        Dictionary containing color maps and commonly used dataframes.
    """

    import os
    import sys
    import plotly.io as pio

    # Make project root importable
    project_root = os.path.abspath(
        os.path.join(os.getcwd(), "..")
    )

    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Plotly configuration
    pio.renderers.default = "notebook_connected"
    pio.renderers[pio.renderers.default].config = {
        "displayModeBar": False
    }

    # Initialize backend data
    initialize_data()

    # Color maps
    player_color_map, archetype_color_map, decktype_color_map = (
        get_color_maps()
    )

    # Common data
    vintage_decks_df = get_vintage_decks()
    decks_with_standings = get_decks_with_standings()

    # Win-rate data
    archetype_game_winrate = get_data("archetype_game_winrate")
    decktype_game_winrate = get_data("decktype_game_winrate")
    archetype_match_winrate = get_data("archetype_match_winrate")
    decktype_match_winrate = get_data("decktype_match_winrate")

    # Filter for all seasons
    archetype_game_winrate = archetype_game_winrate[
        archetype_game_winrate["season_id"] == "Season-All"
    ]

    decktype_game_winrate = decktype_game_winrate[
        decktype_game_winrate["season_id"] == "Season-All"
    ]

    archetype_match_winrate = archetype_match_winrate[
        archetype_match_winrate["season_id"] == "Season-All"
    ]

    decktype_match_winrate = decktype_match_winrate[
        decktype_match_winrate["season_id"] == "Season-All"
    ]

    return {
        "player_color_map": player_color_map,
        "archetype_color_map": archetype_color_map,
        "decktype_color_map": decktype_color_map,
        "vintage_decks_df": vintage_decks_df,
        "decks_with_standings": decks_with_standings,
        "archetype_game_winrate": archetype_game_winrate,
        "decktype_game_winrate": decktype_game_winrate,
        "archetype_match_winrate": archetype_match_winrate,
        "decktype_match_winrate": decktype_match_winrate,
    }
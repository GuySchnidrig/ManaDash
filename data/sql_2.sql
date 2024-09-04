-- Table for storing player names
CREATE TABLE player_names (
    player_name TEXT NOT NULL UNIQUE PRIMARY KEY
);

-- Table for storing deck names
CREATE TABLE deck_names (
    deck_name TEXT NOT NULL UNIQUE PRIMARY KEY
);

-- Table for storing game data
CREATE TABLE game_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    game_type TEXT,
    date TEXT,
    player_name TEXT,
    deck_name TEXT,
    start INTEGER,
    win INTEGER,
    win_turn INTEGER,
    win_type TEXT,
    mv_card TEXT,
    life INTEGER,
    time_total NUMERIC,
    deck_link TEXT,
    uploader TEXT,
    FOREIGN KEY (player_name) REFERENCES player_names (player_name),
    FOREIGN KEY (deck_name) REFERENCES deck_names (deck_name)
);
INSERT OR IGNORE INTO player_names (player_name)
SELECT DISTINCT player_name FROM game_data_old;

INSERT OR IGNORE INTO deck_names (deck_name)
SELECT DISTINCT deck_name FROM game_data_old;

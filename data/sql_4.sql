INSERT INTO game_data (
    game_id,
    game_type,
    date,
    player_name,
    deck_name,
    start,
    win,
    win_turn,
    win_type,
    mv_card,
    life,
    time_total,
    deck_link,
    uploader
)
SELECT
    gdo.game_id,
    gdo.game_type,
    gdo.date,
    gdo.player_name,
    gdo.deck_name,
    gdo.start,
    gdo.win,
    gdo.win_turn,
    gdo.win_type,
    gdo.mv_card,
    gdo.life,
    gdo.time_total,
    gdo.deck_link,
    gdo.uploader
FROM game_data_old gdo
JOIN player_names pn ON gdo.player_name = pn.player_name
JOIN deck_names dn ON gdo.deck_name = dn.deck_name;

import sqlite3
from flask import jsonify
import helpers.sqlite_connect as helper

#route: /games
#method GET
#get all games
def get_games():
    try:
        db = helper.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM game_data")
        results = cursor.fetchall()
        cursor.close()
        return jsonify(results)
    
    except sqlite3.Error as e:
        return jsonify({"error": "Failed to retrieve games: " + str(e)})

#route: /games/<gameID>
#method GET
#get a game
def get_game(gameID):
    pass

#route: /games
#method POST
#create a game
def create_game():
    pass

#route: /games/<gameID>
#method PUT
#update a game
def update_game(gameID):
    pass

#route: /games/<gameID>
#method DELTE
#delete a game
def delete_game(gameID):
    pass

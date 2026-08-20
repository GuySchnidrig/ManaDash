# Import libraries
from flask import g
from datetime import datetime
import json
from collections import OrderedDict
import sqlite3
from dash import Dash, dcc, html

import helpers.sqlite_connect as helper


#route: /players
#method GET
#get all players
def get_players():
    results = []
    message = ""

    try:
        # Establish the database connection
        db = helper.get_db()
        
        # Create a cursor object using the connection
        cursor = db.cursor()
        
        # Execute the query
        cursor.execute("SELECT * FROM player_names")
        
        # Fetch all the results
        results = cursor.fetchall()
        
        # Close the cursor (SQLite connection will be closed at teardown)
        cursor.close()
        
        # Render the template with data
        return results
    
    except sqlite3.Error as e:
        results = ["#"]
        message = "Not connected: " + str(e)
        
        # Render the template with error message
        return message

#route: /players/<playername>
#method GET
#get a player
def get_player(playername):
    pass


#route: /players
#method POST
#create a player
def create_player():
    pass

#route: /players/<playername>
#method PUT
#update a player
def update_player(playername):
    pass

#route: /players/<playername>
#method DELTE
#delete a player
def delete_player(playername):
    pass

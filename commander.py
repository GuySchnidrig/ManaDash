# Import libraries
from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, session, flash, g
from io import StringIO
import os
from datetime import datetime
import json
from collections import OrderedDict
import sqlite3
from dash import Dash, dcc, html

import helpers.sqlite_connect as helper

def commander():
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
        return render_template('commander.html', results=results, message=message)
    
    except sqlite3.Error as e:
        results = ["#"]
        message = "Not connected: " + str(e)
        
        # Render the template with error message
        return render_template('commander.html', results=results, message=message)
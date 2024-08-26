# Import libraries
from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, session, flash, g
from io import StringIO
import os
from datetime import datetime
import json
from collections import OrderedDict
import sqlite3
from dash import Dash, dcc, html


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Get the directory of the currently executing script
script_directory = os.path.dirname(__file__)

# Set the current working directory to the script directory
os.chdir(script_directory)

# Configuration settings
with open('user_credentials.json', 'r') as file:
    data = json.load(file)
    USER_CREDENTIALS = data['USER_CREDENTIALS']
    
# Database configuration
DATABASE = os.path.join(script_directory, 'data', 'cmdr_tracker.db')

def get_db():
    """Open a new database connection if none exists."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


# Routes
@app.route('/')
def index(): 
    if 'logged_in' in session and session['logged_in']:
        return(redirect(url_for('login')))
    else:
        return(redirect(url_for('login')))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USER_CREDENTIALS and password == USER_CREDENTIALS[username]:
            session['logged_in'] = True
            session['username'] = username
            flash("Login successful!", "info")
            return redirect(url_for('entry_screen'))
        else:
            flash("Invalid username or password. Please try again.", "error")
    return render_template('login.html')


@app.route('/entry_screen', methods=['GET', 'POST'])
def entry_screen():
    if 'logged_in' in session and session['logged_in']:
      session['username'] = session['username']
    
    print(session['username'])
    
    return render_template('entry_screen.html')

@app.route('/submit_commander', methods=['POST'])
def submit_commander():
    results = []
    message = ""

    try:
        # Establish the database connection
        db = get_db()
        
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
        

@app.route('/submit_vintage', methods=['POST'] )
def submit_vintage():
    return render_template('vintage.html')


# Remove if pushed to production on www.pythonanywhere.com
if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')
    
    
# 5ETB9t.z7MAg6Nc DB password
# 
# Set DB in MYSQL:
# SOURCE /home/GuySchnidrig/mysite/data/cmdr_tracker.sql;
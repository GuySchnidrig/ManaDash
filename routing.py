# Import libraries
from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, session, flash, g
from io import StringIO
import os
from datetime import datetime
import json
from collections import OrderedDict
import sqlite3
from dash import Dash, dcc, html
from flask_bootstrap import Bootstrap

#import routings
import commander
import cube
import backend.player as player

# Import Dash application
from dash_applcation import create_dash_application

app = Flask(__name__)
app.secret_key = os.urandom(24)

Bootstrap(app)
create_dash_application(app)

# Get the directory of the currently executing script
script_directory = os.path.dirname(__file__)

# Set the current working directory to the script directory
os.chdir(script_directory)

# Configuration settings
with open('user_credentials.json', 'r') as file:
    data = json.load(file)
    USER_CREDENTIALS = data['USER_CREDENTIALS']
    
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

#commander routes
app.add_url_rule('/commander',view_func=commander.commander)

#cube routes
app.add_url_rule('/vintage',view_func=cube.vintage)

#backend routes
app.add_url_rule('/players',view_func=player.get_players)

# Remove if pushed to production on www.pythonanywhere.com
if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')

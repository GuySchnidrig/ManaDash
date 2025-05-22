# Import libraries
from flask import Flask, render_template, request,redirect, url_for, session, flash, g
import os
import json
from flask_bootstrap import Bootstrap
from flask import redirect, url_for, session, request

# Import routings
# import commander
# import cube
import backend.player as player

# Import dash applications
from dash_application_commander import create_dash_application_commander
from dash_application_vintage import create_dash_application_vintage

# Initiate app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Add Boorstrap
Bootstrap(app)

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
    return redirect(url_for('entry_screen')) if session.get('logged_in') else redirect(url_for('login'))

@app.before_request
def require_login():
    allowed_routes = ['login', 'static']
    if not session.get('logged_in') and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))

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

    print(f"Dash apps initialized for user: {session['username']}")

    print(session['username'])
    
    return render_template('entry_screen.html')

@app.route('/redirect_to_flask')
def redirect_to_flask():
    return redirect(url_for('entry_screen'))

#commander routes
# app.add_url_rule('/commander',view_func=commander.commander)
create_dash_application_commander(app)


#cube routes
#app.add_url_rule('/vintage',view_func=cube.vintage)
create_dash_application_vintage(app)

#backend routes
app.add_url_rule('/players',view_func=player.get_players)


# Remove if pushed to production on www.pythonanywhere.com
if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')

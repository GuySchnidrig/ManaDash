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

# Routes
@app.route('/')
def index():
    return redirect(url_for('entry_screen'))

@app.route('/entry_screen', methods=['GET', 'POST'])
def entry_screen():
    print("Dash apps initialized")
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

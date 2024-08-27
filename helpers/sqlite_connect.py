import os
import sqlite3
from flask import g

# Get the directory of the currently executing script
script_directory = os.path.dirname(__file__)

# Set the current working directory to the script directory
os.chdir(script_directory)

# Database configuration
DATABASE = os.path.join(script_directory, '../data', 'cmdr_tracker.db')

def get_db():
    """Open a new database connection if none exists."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db
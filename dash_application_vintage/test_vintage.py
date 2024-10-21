import sqlite3
import pandas as pd
import os
import plotly.express as px
import seaborn as sns
import matplotlib.colors as mcolors
import requests
from dash import html

# Define the path to your SQLite database relative to the root of your project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one directory
DB_PATH = os.path.join(ROOT_DIR, 'data', 'cmdr_tracker_v2.db')

DB_PATH_vintage = os.path.join(ROOT_DIR, 'data', 'vintage_cube.db')

def update_card_image(name):
        # Get the row index from the active cell
        card_name =  name
        
        # Fetch card details from Scryfall API using the card name
        url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
        
        response = requests.get(url)        
        card_data = response.json()
        
        # Check if the card has multiple faces (e.g., double-faced cards)
        if 'image_uris' in card_data:
            # Single-faced card, so we just get the 'normal' image from 'image_uris'
            first_image_url = card_data['image_uris'].get('normal', '')
            second_image_url = None  # No second image in this case
        elif 'card_faces' in card_data:
            # Multi-faced card, so we get images from 'card_faces'
            faces = card_data['card_faces']
            first_image_url = faces[0]['image_uris'].get('normal', '') if len(faces) > 0 else ''
            second_image_url = faces[1]['image_uris'].get('normal', '') if len(faces) > 1 else ''
        else:
            # Neither image_uris nor card_faces are found
            first_image_url = ''
            second_image_url = ''

        # Print the URLs of the first and second image
        print("First image URL (normal):", first_image_url)
        print("Second image URL (normal, if any):", second_image_url)

update_card_image('Ajani, Nacatl Pariah')


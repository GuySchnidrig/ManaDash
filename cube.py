# Import libraries
from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, session, flash, g
from io import StringIO
import os
from datetime import datetime
import json
from collections import OrderedDict
import sqlite3
from dash import Dash, dcc, html

def vintage():
    return render_template('vintage.html')
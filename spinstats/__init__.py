import os

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from spinstats.helpers import format_minutes, format_distance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spinstats.db'
db = SQLAlchemy(app)

# Custom filter
app.jinja_env.filters["format_minutes"] = format_minutes
app.jinja_env.filters["format_distance"] = format_distance

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

from spinstats import routes
from spinstats import models
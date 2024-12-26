from flask import session, redirect
from functools import wraps
from datetime import datetime

emailpattern = r'^[^@]+@[^@]+\.[a-zA-Z]{2,}$'

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def format_minutes(value):
    if value is None:
        return 0
    hours = value // 60
    minutes = value % 60
    return f"{hours:02}:{minutes:02}"

def format_distance(value):
    if value is None:
        return 0
    return value

def validate_ride_data(data):
    distance = data.get('distance')
    elevation = data.get('elevation')
    duration = data.get('duration')
    date = data.get('date')
    error = ""

    if not distance:
            error += "Distance is required.\n"
    try:
        distance = float(distance)
        if not distance > 0:
            error += "Distance must be a positive value.\n"
    except ValueError:
        error += "Distance must be a positive value.\n"

    if not elevation:
        error += "Elevation is required.\n"
    try:
        elevation = float(elevation)
    except ValueError:
        error += "Elevation must be numeric.\n"

    if not duration:
        error += "Duration is required.\n"
    try:
        duration = float(duration)
        if not duration > 0:
            error += "Duration must be a positive value.\n"
    except ValueError:
        error += "Duration must be a positive value.\n"
        
    if not date:
        error += "Date is required.\n"
    try:
        valid_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        error += f"Date must be valid and in format dd/mm/YYYY. Provided: {date}\n"

    if error != "":
        return False, error
    else:
        return True, None
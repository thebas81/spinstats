import re

from flask import flash, request, render_template, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from sqlalchemy import func, desc
from sqlalchemy.exc import IntegrityError

from spinstats import app,db
from spinstats.helpers import login_required, validate_ride_data, emailpattern
from spinstats.models import User, Ride

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = request.form
        username = request.form.get('username')
        email = request.form.get('email')
        name = request.form.get('name')
        location = request.form.get('location')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        error = None

        if not username:
            error = "Username is required."
        elif not name:
            error = "Name is required."
        elif not location:
            error = "Location is required."
        elif not email:
            error = "Email is required."
        elif not re.match(emailpattern, email):
            error = "Email is invalid."
        elif not password:
            error = "Password is required."
        elif not confirmation:
            error = "Confirmation is required."
        elif confirmation != password:
            error = "Password and Confirmation did not match."
        
        if error is None:
            try:
                user = User(username = username, 
                            password = generate_password_hash(password),
                            name = name,
                            email = email,
                            location = location
                            )
                db.session.add(user)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                if 'username' in str(e.orig):
                    error = f"User {username} is already registered."
                elif 'email' in str(e.orig):
                    error = f"Email {email} is already registered."
            else:
                return redirect(url_for('login'))
            
        flash(error)
    
    return render_template('/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        user = User.query.filter_by(username = username).first()

        if not user:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        
        flash(error)
    
    return render_template('/login.html')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(id = session['user_id']).first()
    
    if request.method == 'POST':
        error = None
        try:
            user.email = request.form.get('email')
            user.name = request.form.get('name')
            user.location = request.form.get('location')
            db.session.commit()
        except:
            error = "Error while updating account details."
        
        if error is None:
            return redirect(url_for('account'))
    
        flash(error)
    
    return render_template('/account.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/newride', methods=['GET', 'POST'])
@login_required
def newride():
    if request.method == 'POST':
        is_valid, error = validate_ride_data(request.form)

        if is_valid is not True:
            flash(error)
        else:
            ride = Ride(
                user_id = session['user_id'],
                distance = request.form.get('distance'),
                elevation = request.form.get('elevation'),
                duration = request.form.get('duration'),
                date = datetime.strptime(request.form.get('date'), "%Y-%m-%d")
            )
            db.session.add(ride)
            db.session.commit()
            return redirect(url_for('dashboard'))
        
    return render_template('/newride.html')

@app.route('/<int:id>/updateride', methods=['GET', 'POST'])
@login_required
def updateride(id):
    ride = Ride.query.filter_by(id = id).first()

    if request.method == 'POST':
        is_valid, error = validate_ride_data(request.form)

        if is_valid is not True:
            flash(error)
        else:
            ride.distance = request.form.get('distance')
            ride.elevation = request.form.get('elevation')
            ride.duration = request.form.get('duration')
            ride.date = datetime.strptime(request.form.get('date'), "%Y-%m-%d")
            db.session.commit()
            return redirect(url_for('dashboard'))

    return render_template('/editride.html', ride=ride)

@app.route('/<int:id>/deleteride')
@login_required
def deleteride(id):
    try:
        ride = Ride.query.filter_by(id = id).first()
        db.session.delete(ride)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Error while deleting ride.")
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    rides = Ride.query.filter_by(user_id = session['user_id']).order_by(desc(Ride.date)).limit(10)

    stats = {}
    result = db.session.query(
        func.sum(Ride.distance).label('distance'),
        func.sum(Ride.elevation).label('elevation'),
        func.sum(Ride.duration).label('duration')
        ).filter(
        Ride.user_id == session['user_id'],
        Ride.date >= func.date('now', 'weekday 0', '-7 days'),
        Ride.date < func.date('now', 'weekday 0')
    ).one()

    stats['week'] = {
        'distance': result.distance,
        'elevation': result.elevation,
        'duration': result.duration
    }

    result = db.session.query(
        func.sum(Ride.distance).label('distance'),
        func.sum(Ride.elevation).label('elevation'),
        func.sum(Ride.duration).label('duration')
        ).filter(
        Ride.user_id == session['user_id'],
        Ride.date >= func.date('now', 'start of month'),
        Ride.date < func.date('now', 'start of month', '+1 month')
    ).one()

    stats['month'] = {
        'distance': result.distance,
        'elevation': result.elevation,
        'duration': result.duration
    }

    result = db.session.query(
        func.sum(Ride.distance).label('distance'),
        func.sum(Ride.elevation).label('elevation'),
        func.sum(Ride.duration).label('duration')
        ).filter(
        Ride.user_id == session['user_id'],
        Ride.date >= func.date('now', 'start of year'),
        Ride.date < func.date('now', 'start of year', '+1 year')
    ).one()

    stats['year'] = {
        'distance': result.distance,
        'elevation': result.elevation,
        'duration': result.duration
    }

    result = db.session.query(
        func.sum(Ride.distance).label('distance'),
        func.sum(Ride.elevation).label('elevation'),
        func.sum(Ride.duration).label('duration')
        ).filter(
        Ride.user_id == session['user_id']
    ).one()

    stats['alltime'] = {
        'distance': result.distance if result.distance is not None else 0,
        'elevation': result.elevation if result.elevation is not None else 0,
        'duration': result.duration if result.duration is not None else 0
    }

    if result.distance is not None:
        percent = (result.distance / 40075) * 100
    else:
        percent = 0
    stats['around-the-world'] = {
        'percent': percent
    }
    if result.elevation is not None:
        percent = (result.elevation / 8848) * 100
    else:
        percent = 0
    stats['climb-everest'] = {
        'percent': percent
    }

    return render_template('/dashboard.html', user=user, rides=rides, stats=stats)
from spinstats import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=32), nullable=False, unique=True)
    password = db.Column(db.String(length=64), nullable=False)
    email = db.Column(db.String(length=64), nullable=False, unique=True)
    name = db.Column(db.String(length=32), nullable=False)
    location = db.Column(db.String(length=32), nullable=False)
    rides = db.relationship('Ride', backref='rider', lazy=True)

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    distance = db.Column(db.Integer, nullable=False)
    elevation = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    streak = db.Column(db.Integer, default=0)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    user_id = db.Column(db.Integer)

class DailyTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    diet = db.Column(db.Boolean)
    workout = db.Column(db.Boolean)
    water = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
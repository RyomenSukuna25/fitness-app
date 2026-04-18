from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    user_id = db.Column(db.Integer)

class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diet_done = db.Column(db.Boolean)
    workout_done = db.Column(db.Boolean)
    water = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
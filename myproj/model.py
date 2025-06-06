'''
cherry mercedes
5/21/25

define what data i store, save changes, add new daata, access data

'''

from flask_sqlalchemy import SQLAlchemy
from extensions import db

class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))

    #workouts = db.relationship('Workout', backref='user', lazy=True)
    #weight_log = db.relationship('weight_log', backref='user', lazy=True)


class Workout(db.Model):
    id = db.Column('workout_id', db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))#foreign
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)

    #exercises = db.relationship('Exercise', backref='workout', lazy=True)

class Exercise(db.Model):

    id = db.Column('exercise_id', db.Integer, primary_key = True, autoincrement=True)
    workout_id = db.Column('workout_id', db.Integer, db.ForeignKey('workout.workout_id'))
    exercise = db.Column(db.String(50), nullable=False)
    reps = db.Column(db.Integer(), nullable=False)
    sets = db.Column(db.Integer(), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)


#class Time_log():

class Weight_log(db.Model): 
    id = db.Column('weight_id', db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))#foreign
    date = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)

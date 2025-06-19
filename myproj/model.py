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

#workout session: exleg day 6/16
class Workout(db.Model):
    id = db.Column('workout_id', db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))#foreign
    name = db.Column(db.String(50), nullable=False)
    datetime = db.DateTime

class Exercise(db.Model): #master exercise list
    id = db.Column('exercise_id', db.Integer, primary_key = True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))#foreign
    exercise = db.Column(db.String(50), nullable=False)

#tracking whats done in the workout/what happened within it
class WorkoutExercise(db.Model):
    id = db.Column('exercise_id', db.Integer, primary_key = True, autoincrement=True)
    workout_id = db.Column('workout_id', db.Integer, db.ForeignKey('workout.workout_id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'))
    reps = db.Column(db.Integer(), nullable=False)
    sets = db.Column(db.Integer(), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)

#class Time_log():

class Weight_log(db.Model): 
    id = db.Column('weight_id', db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))#foreign
    date = db.Date
    weight = db.Column(db.Integer(), nullable=False)

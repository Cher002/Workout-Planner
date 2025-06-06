#5/20/25
#workoutplanner
#server - flask, route logic, API endpoints

import os, datetime

from flask import Flask, render_template, session, redirect, url_for, jsonify, request,  abort  
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from model import *
#url_for('static', filename = 'style.css')

app = Flask(__name__, instance_relative_config = True)
app.config['SECRET_KEY'] = 'bangtansonyeondanhandulset'

#connecting database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'data', 'workout.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

db.init_app(app)


#route() to bind function to a URL
@app.route('/', methods = ['GET']) 
def index():
    return render_template('index.html', utc_dt = datetime.datetime.utcnow())


@app.route('/user/<username>')
def show_user_profile(username):
    return f'{username}\'s profile'
    #return f'User {escape(username)}'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':


        loged_user = User.query.filter_by(username = request.form['username']).first()
        if loged_user is None:
            return redirect('/login')
       
        if request.form['password'] == loged_user.password: 
            #store user's id in the sesssion \
            session['user_id'] = loged_user.id
            return redirect(url_for('index')) #will set the login session  and redirect 
        else:
            return render_template('login.html', t = 'Incorrect Password')

    else:
        return render_template('login.html', utc_dt = datetime.datetime.utcnow())



@app.route('/create_account', methods = ['GET'])
def show_create_account():
    return render_template("create_account.html")

@app.route('/create_account', methods = ['POST'])
def create_account():
    username = request.form['username'] #storing the users input
    password = request.form['password']
   # repass = request.form[]
    email = request.form['email']

    print(f"username {username} : pass {password}")

    #SAVE TO DATABASE:
    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/create_account')
    

@app.route('/about/')
def about():
    return  render_template('about.html', utc_dt = datetime.datetime.utcnow())


@app.route('/add_exercise', methods = ['GET'])
def show_add_exercise():
    return render_template("exercise.html")

@app.route('/add_exercise', methods = ['POST'])
def add_exercise():
    exercise = request.form['exercise']
    reps = request.form['reps']
    sets = request.form['sets']
    weight = request.form['weight']
    print(f"Exercise {exercise} : Reps {reps}" )

    #save to DATABASE
    new_exercise = Exercise(exercise=exercise, reps=reps, sets=sets, weight=weight)
    db.session.add(new_exercise)
    db.session.commit()

    session['exercise_id'] = new_exercise.id#???

    return redirect('/')#get_exercise



@app.route('/test/')
def test():
    test = ['UNOOOOO', 'two', 'threee']
    return render_template("test.html", test=test)


@app.route('/get_workouts')
def get_workouts():
    workout = jsonify([w.to_dict() for w in Workout.query.all()])
    return render_template("workouts.html", workout=workout)
'''
@app.route('/get_exercise')
def get_exercise():
    exercise = jsonify([e.to_dict() for e in Exercise.query.all()])
    return redirect('/')
   # return render_template("exercise.html", exercise=exercise)
'''



if __name__ == "__main__":
    with app.app_context():
        db.create_all()#will create the tables that are in info.py
    app.run(debug = True)
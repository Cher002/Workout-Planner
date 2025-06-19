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
    user = None 
    if 'user_id' in session:
        user = User.query.get(session['user_id'])#retrievethe username
    return render_template('index.html', utc_dt = datetime.datetime.utcnow(), user=user)


@app.route('/user/<username>')
def show_user_profile(username):
    return f'{username}\'s profile'



@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        #checking if user even exists
        loged_user = User.query.filter_by(username = request.form['username']).first()
        if loged_user is None:      #user doesnt exists
            return render_template('login.html', t = 'username doesnt exists')
       
        #check if password matches one in database
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
    user_new = User.query.filter_by(username = request.form['username']).first() #storing the users input
    password = request.form['password']
    email = request.form['email']

    if user_new is None:
        #SAVE TO DATABASE:
        username = request.form['username']
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    else:
        return render_template('create_account.html', t = 'Username exists, please choose a different one')

    
    

@app.route('/about/')
def about():
    return  render_template('about.html', utc_dt = datetime.datetime.utcnow())


@app.route('/add_exercise', methods = ['GET'])
def show_add_exercise():
    return render_template("exercise.html")

@app.route('/add_exercise', methods = ['POST'])
def add_exercise():

    if 'user_id' not in session:
        return redirect('/login')

    exercise_name = request.form['exercise'].strip()
    user_id = session['user_id']

    exer = Exercise.query.filter_by(exercise=exercise_name, user_id=user_id).first()

    if exer is None:
        #add new exercise to db
        new_exer = Exercise(exercise=exercise_name, user_id=user_id)
        db.session.add(new_exer)
        db.session.commit()
        exercise_id = new_exer.id

    else:    #exercise exists, retrieve exercise id
        exercise_id = exer.id

    reps = request.form['reps']
    sets = request.form['sets']
    weight = request.form['weight']
    print(f"Exercise {exercise_name} : Reps {reps}" )
   # time = utc_dt = datetime.datetime.utcnow()

    #save to DATABASE
    new_exercise = WorkoutExercise(exercise_id=exercise_id, reps=reps, sets=sets, weight=weight)
    db.session.add(new_exercise)
    db.session.commit()

    session['exercise_id'] = new_exercise.id#???

    return render_template('exercise.html')



@app.route('/test/')
def test():
    test = ['', '', '']
    return render_template("test.html", test=test)


@app.route('/get_workouts')
def get_workouts():
    workout = Workout.query.all()
    return render_template("workouts.html", workout=workout)


@app.route('/get_exercise', methods=['GET', 'POST'])
def get_exercise():
    
    exercises = Exercise.query.all()
    print("exercise in db: ", Exercise.query.all())
    print("exercise passed to template:", exercises)  

    #if request.method = "POST":
     #   print(request.form.getlist('selected_exercises'))

    #save selected exercises to a workout

    return render_template("workouts.html", exercises=exercises, t= 'Select your exercises')

    


if __name__ == "__main__":
    with app.app_context():
        db.create_all()#will create the tables that are in info.py
    app.run(debug = True)
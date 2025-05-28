#5/20/25
#workoutplanner
#server

import os
from flask import Flask  
from markupsafe import escape
from flask import url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy


#url_for('static', filename = 'style.css')

app = Flask(__name__, instance_relative_config = True)

#connecting database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'data', 'workout.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#route() to bind function to a URL
@app.route('/') 
def index():
    return render_template('index.html')



@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def show_user_profile(username):
    return f'{username}\'s profile'
    #return f'User {escape(username)}'

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
"""

@app.route('/about')
def about():
    return 'The about page'


@app.route('/api/workouts')
def get_workouts():
    return jsonify([w.to_dict() for w in Workout.query.all()])



"""
with app.test_request_context():
    print(url_for('profile', username = 'john smith'))
"""

with app.app_context():
    db.create_all()#will create the tables that are in info.py


if __name__ == "__main__":
    app.run(debug = True)
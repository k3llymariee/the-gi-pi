from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, date, timedelta
import json

from model import db, connect_to_db, User, Food, FoodIngredient, Ingredient, Symptom, SymptomLog, FoodLog, SymptomFood
from nutritionix import search


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "super-secret"

# raise an error in Jinja2 when using an undefined variable
app.jinja_env.undefined = StrictUndefined

# current date needed to default homepage to today's date
current_date = (date.today()).strftime('%Y-%m-%d')

def forward_day(date_string):
    """Returns a string value of one day ahead given a string date input"""

    day_value = datetime.strptime(date_string, '%Y-%m-%d')

    return (day_value + timedelta(days=1)).strftime('%Y-%m-%d')

def backward_day(date_string):
    """Returns a string value of one day before given a string date input"""
    day_value = datetime.strptime(date_string, '%Y-%m-%d')

    return (day_value + timedelta(days=-1)).strftime('%Y-%m-%d')


@app.route('/')
def index():
    """Defaults user view to today's log entries"""

    next_day = forward_day(current_date)
    day_before = backward_day(current_date)

    return render_template(
                        'daily_view.html', 
                        selected_date=current_date,
                        day_forward=next_day,
                        day_backward=day_before,
                        current_date=current_date,
                        )


@app.route(f"/<selected_date>")
def daily_view(selected_date=current_date):
    """Daily view of foods eaten"""

    next_day = forward_day(selected_date)
    day_before = backward_day(selected_date)

    return render_template(
                        'daily_view.html', 
                        selected_date=selected_date,
                        day_forward=next_day,
                        day_backward=day_before,
                        current_date=current_date,
                        )


@app.route('/register')
def register_form():
    """Show form for user signup"""

    return render_template('register_form.html')

@app.route('/register', methods=['POST'])
def register_process():

    register_form = request.form 


    if User.query.filter(User.email == register_form['email']).first():
        flash('Email already exists within our userbase')
        return redirect('/register')

    elif register_form['password'] != register_form['confirm_password']:
        flash('Passwords do not match')
        return redirect('/register')

    else:
        new_user = User(email=register_form['email'], password=register_form['password'])
        db.session.add(new_user)
        db.session.commit()
        flash('Added new user')
        session['user_email'] = register_form['email']
        flash('Successfully logged in')
        return redirect('/')


@app.route("/login", methods=['GET'])
def login_form():
    """Show login form"""

    return render_template('login.html')

@app.route("/login", methods=['POST'])
def process_login():
    """Log a user in if the user is in the database and provides correct password"""

    login_attempt = request.form

    user = User.query.filter(User.email == login_attempt['email']).first()

    # check if a user exists in the database
    if not user:
        flash('Incorrect email')
        return redirect("/login")

    # check if their password matches
    elif user.password != login_attempt['password']:
        flash('Incorrect password')
        return redirect("/login")

    # if yes to both above, add user_id to session data
    else:
        session['user_email'] = login_attempt['email']
        flash('Successfully logged in')
        return redirect('/')


@app.route("/logout")
def process_logout():

    del session['user_email']

    return redirect("/login")

@app.route("/add_food/<meal>/<selected_date>")
def add_food(meal, selected_date):

    return render_template('add_food.html', meal=meal, selected_date=selected_date)


@app.route("/food_search/<search_term>")
def database_search(search_term):
    """Search for a food given a user's input"""

    # search_term = request.args.get('search_term')

    results = search(search_term)  # returns a dictionary of results

    branded_foods = results['branded']  # returns a list of branded foods

    return jsonify({"foods": branded_foods})


@app.route("/add_symptom")
def symptom_form():

    symptoms = Symptom.query.all()

    return render_template('add_symptom.html', symptoms=symptoms, current_time=datetime.today())


@app.route("/add_symptom", methods=['POST'])
def add_symptom():

    user = User.query.filter(User.email == session['user_email']).first()

    symptom = request.form.get('symptom')
    time = request.form.get('symptom_time')

    new_symptom = Symptom(name=symptom)
    db.session.add(new_symptom)
    db.session.commit()  # commit first in order to get user_id
    symptom_log = SymptomLog(ts=time, symptom_id=new_symptom.id, user_id=user.id)
    db.session.add(symptom_log)
    db.session.commit()

    return redirect("/")


if __name__ == "__main__":

    # Remove debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
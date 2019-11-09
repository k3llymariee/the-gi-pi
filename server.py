from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, date, timedelta
import json

from model import db, connect_to_db, User, Food, FoodIngredient, Ingredient, Symptom, SymptomLog, FoodLog, UserSymptomFoodLink, Meal
from nutritionix import search
from sqlalchemy import extract

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "super-secret"

# raise an error in Jinja2 when using an undefined variable
app.jinja_env.undefined = StrictUndefined

def forward_day(date_string):
    """Returns a string value of one day ahead given a string date input"""

    day_value = datetime.strptime(date_string, '%Y-%m-%d')
    return (day_value + timedelta(days=1)).strftime('%Y-%m-%d')

def backward_day(date_string):
    """Returns a string value of one day before given a string date input"""
    
    day_value = datetime.strptime(date_string, '%Y-%m-%d')
    return (day_value + timedelta(days=-1)).strftime('%Y-%m-%d')

debug = '\n' * 3


@app.route('/')
def index():
    """Defaults user view to today's log entries"""

    # current date needed to default homepage to today's daily view
    current_date = (date.today()).strftime('%Y-%m-%d')

    if not session.get('user_id'):
        return redirect("/register")

    else:
        return redirect(f'/{current_date}')


@app.route(f"/<selected_date>")
def daily_view(selected_date):
    """Daily view of foods eaten"""

    user = User.query.get(session['user_id'])
    meals = Meal.query.all()

    day_value = datetime.strptime(selected_date, '%Y-%m-%d')
    user_foods = FoodLog.query.join(Food).filter(extract('year', FoodLog.ts) == day_value.year,
                                                 extract('month', FoodLog.ts) == day_value.month,
                                                 extract('day', FoodLog.ts) == day_value.day,
                                                 FoodLog.user_id == user.id).all()
    
    day_end = datetime.strptime(selected_date +' 23:59:59', '%Y-%m-%d %H:%M:%S')
    user_symptoms = SymptomLog.query.join(Symptom).filter(SymptomLog.ts.between(day_value, day_end),
                                                 SymptomLog.user_id == user.id).all()

    return render_template(
                        'daily_view.html', 
                        selected_date=day_value.strftime("%A, %B %d"),
                        day_forward=forward_day(selected_date),
                        day_backward=backward_day(selected_date),
                        # current_date=date.today().strftime('%Y-%m-%d'),
                        user_foods=user_foods,
                        user_symptoms=user_symptoms,
                        meals=meals,
                        )


@app.route('/register', methods=['GET'])
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
        new_user = User(email=register_form['email'],
                        password=register_form['password'])
        db.session.add(new_user)
        db.session.commit()
        flash('Added new user')

        session['user_id'] = new_user.id
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
        session['user_id'] = user.id
        flash('Successfully logged in')
        return redirect('/')


@app.route("/logout")
def process_logout():
    """Log a user out by deleting their session variable"""

    del session['user_id']
    return redirect("/login")

@app.route("/add_food", methods=['GET'])
def add_food_form():
    """Displays the general add food template"""

    return render_template('add_food.html')

@app.route("/add_food", methods=['POST'])
def add_food_to_log():
    """Commit food to DB logs"""

    food = Food.query.get(request.form.get('food_id'))
    time = request.form.get('time_eaten')
    user = User.query.get(session['user_id'])
    meal = Meal.query.get(request.form.get('meal_to_add'))
    time_value = datetime.strptime(time, '%Y-%m-%dT%H:%M')


    food_log_entry = FoodLog(meal=meal, 
                             food_id=food.id, 
                             user_id=user.id, 
                             ts=time_value,
                             )

    db.session.add(food_log_entry)
    db.session.commit()

    return redirect("/")

@app.route("/add_food/<food_id>")
def confirm_add_food_to_log(food_id):
    """Confirms which food selected food(s) to users food log"""

    food = Food.query.get(food_id)
    user = User.query.get(session['user_id'])
    meals = Meal.query.all()
    return render_template('confirm_food.html', food=food, meals=meals)


@app.route("/food_search/<search_term>")
def nutrionix_search(search_term):
    """Search nutritionix API for a food given a user's input"""

    results = search(search_term)  # returns a dictionary of results from API
    branded_foods = results['branded']  # returns a list of branded foods
    return jsonify({"foods": branded_foods})  # jsonify the list to pass thru


@app.route("/user_foods.json")
def search_user_foods():

    user = User.query.get(session['user_id'])

    # only show foods that the user has eating recently
    user_foods = FoodLog.query.filter(FoodLog.user_id == user.id).order_by(FoodLog.ts.desc()).limit(10)
    # TODO: update query to pull only distinct foods for the case when 
    # a user has eaten the same thing more than once recently 

    foods = []
    for food in user_foods:
        foods.append({'name': food.food.name, 
                      'brand': food.food.brand_name, 
                      'id': food.food.id,
                      })

    return jsonify({"foods": foods})

@app.route("/db_food_search/<search_term>")
def database_search(search_term):
    """Search existing database for a food given a user's input"""

    user = User.query.get(session['user_id'])

    # search demo database FIRST, from any user
    database_foods = Food.query.filter(Food.name.ilike(f'%{search_term}%')).all()

    foods = []
    for food in database_foods:
        foods.append({'food': food.name, 
                      'brand': food.brand_name,
                      'id': food.id})

    return jsonify({"foods": foods})


@app.route("/manual_add", methods=['GET'])
def manually_add_form():

    meals = Meal.query.all()

    return render_template('manual_add.html', meals=meals)

@app.route("/manual_add", methods=['POST'])
def manually_add_food():
    """Add food to foods, ingredient to ingredients, and food log event to DB"""

    # add food to foods table
    new_food = Food.add_or_return_food(food_name=request.form.get('food_name'), 
                                       brand_name=request.form.get('brand_name'))

    if not new_food:  # add_or_return returns false if food exists
        flash("Food already exists within DB")
        return redirect('/manual_add')

    # add ingredients and link them to the food
    new_food.add_ingredients_and_links(request.form.get('ingredients'))

    # add meal to food log
    new_food_log = FoodLog(meal_id=request.form.get('meal_to_add'), 
                           food_id=new_food.id, 
                           user_id=session['user_id'],
                           ts=request.form.get('time_eaten'))
    db.session.add(new_food_log)

    db.session.commit()

    return redirect("/")


@app.route("/add_symptom", methods=['GET'])
def symptom_form():
    """Display form for users to add their symptoms"""

    symptoms = Symptom.query.all()
    return render_template('add_symptom.html', 
                            symptoms=symptoms, 
                            # current_time=datetime.today(),
                            )


@app.route("/add_symptom", methods=['POST'])
def add_symptom():

    user = User.query.filter(User.id == session['user_id']).first()

    symptom_log = SymptomLog(ts=request.form.get('symptom_time'), 
                             symptom_id=request.form.get('symptom_to_add'), 
                             user_id=user.id)

    db.session.add(symptom_log)
    db.session.commit()

    symptom_log.match_foods()
    
    return redirect("/")


if __name__ == "__main__":

    # Remove debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
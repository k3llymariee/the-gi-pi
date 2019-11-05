from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, date, timedelta

from model import connect_to_db
from nutritionix import search


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "super-secret"

# raise an error in Jinja2 when using an undefined variable
app.jinja_env.undefined = StrictUndefined

# current date needed to default homepage to today's date
current_date = (date.today()).strftime('%Y-%m-%d')

def forward_day(date_string):
    """Returns a string value of one day forward given a string date input"""

    day_value = datetime.strptime(date_string, '%Y-%m-%d')

    return (day_value + timedelta(days=1)).strftime('%Y-%m-%d')

def backward_day(date_string):

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

@app.route("/login", methods=['GET'])
def login_form():
    """Show login form"""

    return render_template('login.html')

@app.route("/login", methods=['POST'])
def process_login():
    """Log a user in if the user is in the database and provides correct password"""

    login_attempt = request.form

    # check if a user exists in the database

    # check if their password matches

    # if yes to both above, add user_id to session data

    session['user_email'] = login_attempt['email']

    return redirect('/')

@app.route("/add_food/<meal>/<selected_date>")
def add_food(meal, selected_date):

    return render_template('add_food.html', meal=meal, selected_date=selected_date)


@app.route("/food_search/<meal>/<selected_date>")
def database_search(meal, selected_date):
    """Search for a food given a user's input"""

    search_term = request.args.get('search_term')

    return search(search_term)

if __name__ == "__main__":

    # Remove debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
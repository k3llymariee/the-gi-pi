from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, date, timedelta

from model import connect_to_db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "super-secret"

# raise an error in Jinja2 when using an undefined variable
app.jinja_env.undefined = StrictUndefined

# current date needed to default homepage to today's date
current_date = (date.today()).strftime('%Y-%m-%d')

@app.route('/')
def index():
    """Defaults user view to today's log entries"""

    return redirect(f"/{current_date}")


@app.route(f"/<selected_date>")
def daily_view(selected_date=current_date):
    """Daily view of foods eaten"""

    day_value = datetime.strptime(selected_date, '%Y-%m-%d')

    day_forward = (day_value + timedelta(days=1)).strftime('%Y-%m-%d')
    day_backward = (day_value + timedelta(days=-1)).strftime('%Y-%m-%d')

    return render_template(
                        'daily_view.html', 
                        selected_date=selected_date,
                        day_forward=day_forward,
                        day_backward=day_backward,
                        current_date=current_date,
                        )

@app.route("/login", methods=['GET'])
def login_form():
    """Show login form"""

    return render_template('login.html')

@app.route("/login", methods=['POST'])
def process_login():
    """Log a user in if the user is in the database and provides correct password"""

    pass

if __name__ == "__main__":

    # Remove debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
# Models and database functions 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///demo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users in the system"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):

        return f"<User id={self.id} email={self.email}>"


class Food(db.Model):
    """Foods added to the database by users"""

    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    brand_name = db.Column(db.String(200), nullable=True)

    ingredients = db.relationship('Ingredient', 
                                   secondary='food_ingredients',
                                   backref='foods')

    
    def __repr__(self):
        """Human readable representation of a Food object"""

        return f"<Food food_id={self.id} brand={self.brand_name} food_name={self.name}>"


class Ingredient(db.Model):
    """Ingredients within the database"""

    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


    def __repr__(self):

        return f"<Ingredient id={self.id} name={self.name}>"


class FoodIngredient(db.Model):
    """Tracks the relationship of food items and ingredients"""

    __tablename__ = 'food_ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)


    def __repr__(self):

        return f"<FoodIngredient id={self.id} food_id={self.food_id}>"


class Symptom(db.Model):
    """Symptoms added to the database either as defaults, or user-added"""

    __tablename__ = 'symptoms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        """Human readable representation of a Symptom object"""

        return f"<Symptom symptom_id={self.id} name={self.name}>"


class FoodLog(db.Model):
    """Instances of food consumed by users"""

    __tablename__ = 'food_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ts = db.Column(db.DateTime, nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    food = db.relationship('Food', backref='food_logs')
    user = db.relationship('User', backref='food_logs')
    meal = db.relationship('Meal', backref='food_logs')


    def __repr__(self):

        return f"<FoodLog id={self.id} date={self.ts} meal={self.meal}>"

class Meal(db.Model):

    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)


class SymptomLog(db.Model):
    """Foods in the database"""

    __tablename__ = 'symptom_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ts = db.Column(db.DateTime, nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    symptom = db.relationship('Symptom', backref='symptom_logs')
    user = db.relationship('User', backref='symptom_logs')


    def __repr(self):

        return f"<SymptomLog id={self.id} symtpom_id={self.symptom_id}>"


class UserSymptomFoodLink(db.Model):
    """Correlates foods with symptoms"""

    __tablename__ = 'user_symptom_food_links'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ts = db.Column(db.DateTime, nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptom_logs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food_logs.id'), nullable=False)

    symptom = db.relationship('SymptomLog', backref='user_symptom_food_links')
    user = db.relationship('User', backref='user_symptom_food_links')
    food = db.relationship('FoodLog', backref='user_symptom_food_links')


    def __repr__(self):

        return f"<SymptomFood id={self.id} date={self.ts}>"



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
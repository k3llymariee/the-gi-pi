from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import re

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
    timezone = db.Column(db.String(50), default="America/Los_Angeles")

    foods = db.relationship('Food', 
                             secondary='food_logs',
                             backref='users')

    symptoms = db.relationship('Symptom', 
                             secondary='symptom_logs',
                             backref='users')

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

    @classmethod
    def add_or_return_food(cls, food_name, brand_name=None):
        """Check first if a food already exists within the DB to return warning,
        otherwise create a new food instance"""

        existing_food = Food.query.filter(Food.name == food_name,
                                          Food.brand_name == brand_name,
                                          ).first()
        
        if existing_food:
            return False

        else:
            new_food = cls(name=food_name, brand_name=brand_name)
            db.session.add(new_food)
            db.session.commit()
            return new_food
    

    def add_ingredients_and_links(self, ingredient_str):
        """Given a string 'list' of ingredients (separated by commas), 
        create new ingredient objects and link to food_ingredients table

        Ingredients will always be added at the same time a food is added
        """
        
        ingredient_list = re.findall(r"[\w?\s\w+]+", ingredient_str)

        for ingredient in ingredient_list:

            ingredient = ingredient.lower().strip()
            if ingredient[-3] == 'oes':  #tomatoes, potatoes >> tomato, potato
                ingredient = ingredient[-2]
            if ingredient[-1] == 's':   # seeds, bananas >> seed, banana
                ingredient = ingredient[:-1]
            ingredient = ''.join(c for c in ingredient if c not in '*()')

            existing_ingredient = Ingredient.query.filter(Ingredient.name == 
                                  ingredient).first()

            if existing_ingredient:
                self.ingredients.append(existing_ingredient)
            else: 
                self.ingredients.append(Ingredient(name=ingredient))

        db.session.commit()

    
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
    window_minutes = db.Column(db.Integer, default=180)

    def find_matched_foods(self, user_id):

        symptom_logs = SymptomLog.query.filter(SymptomLog.symptom_id == self.id,
                                               SymptomLog.user_id == user_id).all()

        food_logs = []
        for log in symptom_logs:
            foods.extend(log.match_foods())

        return food_logs


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

        return f"<FoodLog id={self.id} date={self.ts} meal={self.meal_id}>"

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

    def match_foods(self):
        """Given a symtpom log event, find foods eaten within a 3 hour window"""

        window_begin = self.ts + timedelta(hours=-3)

        matched_foods = FoodLog.query.filter(FoodLog.user == self.user,
                                          FoodLog.ts.between(window_begin, self.ts)).all()

        for food in matched_foods:
            new_link = UserSymptomFoodLink(ts=self.ts, 
                                           symptom_id=self.id,
                                           user_id=self.user_id, 
                                           food_id = food.id)
            db.session.add(new_link)

        db.session.commit()

        return matched_foods


    def __repr(self):

        return f"<SymptomLog id={self.id} symtpom_id={self.symptom_id}>"


class UserSymptomFoodLink(db.Model):
    """Correlates foods with symptoms"""

    __tablename__ = 'user_symptom_food_links'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
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
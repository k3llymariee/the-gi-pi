from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from magic import return_ingredient_list
from sqlalchemy import extract

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


def connect_to_db(app, db_uri="postgresql:///demo"):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
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
    timezone = db.Column(db.String(50), default="America/Los_Angeles", nullable=False)

    foods = db.relationship('Food', 
                             secondary='food_logs',
                             backref='users')

    symptoms = db.relationship('Symptom', 
                             secondary='symptom_logs',
                             backref='users')
    
    # TODO: add ingredients relationship
    def get_daily_food_logs(self, selected_date):
        """Return food logs for a specific date"""
        day_value = datetime.strptime(selected_date, '%Y-%m-%d')

        daily_food_logs = FoodLog.query \
                          .filter(extract('year', FoodLog.ts) == day_value.year,
                                  extract('month', FoodLog.ts) == day_value.month,
                                  extract('day', FoodLog.ts) == day_value.day,
                                  FoodLog.user_id == self.id) \
                          .all()

        return daily_food_logs

    def get_all_food_logs(self):
        """Return all food logs for a user"""

        daily_food_logs = FoodLog.query \
                          .filter(FoodLog.user_id == self.id) \
                          .all()

        return daily_food_logs

    def return_foods(self):
        """For a given user, return distinct food items they've eaten in order
        of most recently eaten"""

        user_foods = db.session.query(Food).distinct() \
                     .join(FoodLog) \
                     .filter(FoodLog.user_id == self.id) \
                     .order_by(FoodLog.ts.desc()) \
                     .limit(10).all()

        return user_foods

    def return_symptoms(self):
        """For a given user, return all the symptoms they've experienced"""

        distinct_symptoms = db.session.query(Symptom).distinct() \
                            .join(UserSymptomIngredientLink) \
                            .filter(UserSymptomIngredientLink.user_id == self.id) \
                            .all() # TODO: consider setting limits on all .all()'s
        
        return distinct_symptoms
        

    def return_symptom_logs(self, symptom_id):
        """For a user and a specific symptom, return 15 most recent instances of 
        that user experiencing the symptom"""

        symptom_experiences = SymptomLog.query.filter \
                         (SymptomLog.user_id == self.id, 
                          SymptomLog.symptom_id == symptom_id) \
                         .order_by(SymptomLog.ts.desc()) \
                         .limit(15).all()

        return symptom_experiences

    def return_all_symptom_logs(self):
        """For a user and a specific symptom, return 15 most recent instances of 
        that user experiencing the symptom"""

        symptom_experiences = SymptomLog.query.filter \
                         (SymptomLog.user_id == self.id) \
                         .order_by(SymptomLog.ts.desc()) \
                         .all()

        return symptom_experiences


    def return_intolerances(self):
        """For a given user, return all the symptom ingredient links"""

        intolerances = UserSymptomIngredientLink.query \
                       .filter(UserSymptomIngredientLink.user_id == self.id)

        return intolerances


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

        # TODO: it's weird that you're returning two different things :thinking_face:
        existing_food = Food.query.filter(Food.name == food_name,
                                          Food.brand_name == brand_name) \
                                          .first()
        
        if existing_food:  # TODO: consider breaking this true/false as a separate function
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
        
        ingredient_list = return_ingredient_list(ingredient_str)

        for ingredient in ingredient_list:
            existing_ingredient = Ingredient.query \
                                    .filter(Ingredient.name == ingredient) \
                                    .first()

            if existing_ingredient: 
                self.ingredients.append(existing_ingredient)
            else: 
                self.ingredients.append(Ingredient(name=ingredient))

        db.session.commit()

        return None

    
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
    ingredient_id = db.Column(db.Integer, 
                              db.ForeignKey('ingredients.id'), 
                              nullable=False)


    def __repr__(self):

        return f"<FoodIngredient id={self.id} food_id={self.food_id}>"


class Symptom(db.Model):
    """Symptoms added to the database either as defaults, or user-added"""

    __tablename__ = 'symptoms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    window_minutes = db.Column(db.Integer, default=180)
    display_color = db.Column(db.String(7))

    def find_matched_foods(self, user_id):

        # TODO: look at the return type - if you're looking for ingredients, it should
        # be on the ingredients

        symptom_logs = SymptomLog.query.filter(SymptomLog.symptom_id == self.id,
                                               SymptomLog.user_id == user_id) \
                                              .all()

        food_logs = []

        # combines all food logs from all symptom log events
        for symptom_log in symptom_logs:
            food_logs.extend(symptom_log.match_foods(self.window_minutes))  #match foods for symptom LOG

        # create a list of ingredient lists for comparison 
        ingredient_lists_list = [] 
        for food_log in food_logs:
            ingredient_lists_list.append(food_log.food.ingredients)

        return ingredient_lists_list  # finds foods for all food logs for one SYMPTOM


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

    food = db.relationship('Food')
    user = db.relationship('User', backref='food_logs')
    meal = db.relationship('Meal')


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
    severity = db.Column(db.Integer, nullable=True)

    symptom = db.relationship('Symptom', backref='symptom_logs')
    user = db.relationship('User', backref='symptom_logs')

    def match_foods(self, window_minutes):
        """Given a symptom log event, find food_logs within a 3 hour window"""

        window_begin = self.ts - timedelta(minutes=window_minutes)

        matched_food_logs = FoodLog.query \
                            .filter(FoodLog.user == self.user,
                            FoodLog.ts.between(window_begin, self.ts)) \
                            .all()

        return matched_food_logs


    def __repr(self):

        return f"<SymptomLog id={self.id} symtpom_id={self.symptom_id}>"


class UserSymptomIngredientLink(db.Model):
    """Correlates foods with symptoms"""

    __tablename__ = 'user_symptom_ingredient_links'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)

    symptom = db.relationship('Symptom', backref='user_symptom_food_links')
    user = db.relationship('User', backref='user_symptom_food_links')
    ingredient = db.relationship('Ingredient', backref='user_symptom_food_links')


    def __repr__(self):

        return f"<SymptomFood id={self.id}>"

def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB")

def example_data():
    """Create sample data for testing"""
    db.create_all()
    # In case this is run more than once, empty out existing data
    User.query.delete()
    Food.query.delete()
    Ingredient.query.delete()
    Symptom.query.delete()
    FoodIngredient.query.delete()
    FoodLog.query.delete()
    SymptomLog.query.delete()
    UserSymptomIngredientLink.query.delete()

    # Add sample user
    user_1 = User(id=1, email='john@doe.com', password='fluffy89')

    # Add base list symptoms
    symp_1 = Symptom(id=1, name='heartburn')
    symp_2 = Symptom(id=2, name='migraine')
    symp_3 = Symptom(id=3, name='nausea')
    symp_4 = Symptom(id=4, name='indigestion')
    symp_5 = Symptom(id=5, name='upset stomach')

    # Add meals
    meal_1 = Meal(id=1, name='breakfast')
    meal_2 = Meal(id=2, name='lunch')
    meal_3 = Meal(id=3, name='dinner')
    meal_4 = Meal(id=4, name='snacks')

    # Add sample food
    food_1 = Food(id=1, name='Pumpkin Chia Pudding', brand_name='Thistle')

    # Add sample ingredients
    ingrd_1 = Ingredient(id=1, name='hemp milk')
    ingrd_2 = Ingredient(id=2, name='pumpkin')
    ingrd_3 = Ingredient(id=3, name='banana')
    ingrd_4 = Ingredient(id=4, name='maple syrup')
    ingrd_5 = Ingredient(id=5, name='chia seeds')
    ingrd_6 = Ingredient(id=6, name='pea protein powder')
    ingrd_7 = Ingredient(id=7, name='orange zest')

    db.session.add_all([user_1, symp_1, symp_2, symp_3, symp_4, symp_5, meal_1, 
                        meal_2, meal_3, meal_4, food_1, ingrd_1, ingrd_2, 
                        ingrd_3, ingrd_4, ingrd_5, ingrd_6, ingrd_7, 
                        ])
    db.session.commit()

    # Link ingredients to food
    food_ingrd_1 = FoodIngredient(id=1, food_id=1, ingredient_id=1)
    food_ingrd_2 = FoodIngredient(id=2, food_id=1, ingredient_id=2)
    food_ingrd_3 = FoodIngredient(id=3, food_id=1, ingredient_id=3)
    food_ingrd_4 = FoodIngredient(id=4, food_id=1, ingredient_id=4)
    food_ingrd_5 = FoodIngredient(id=5, food_id=1, ingredient_id=5)
    food_ingrd_6 = FoodIngredient(id=6, food_id=1, ingredient_id=6)
    food_ingrd_7 = FoodIngredient(id=7, food_id=1, ingredient_id=7)

    # Add a sample food log
    food_log_1 = FoodLog(id=1, ts=datetime(2019, 11, 27, 8, 0, 0), meal_id=1, user_id=1, food_id=1)

    # Add a sample symptom log
    symptom_log_1 = SymptomLog(id=1, ts=datetime(2019, 11, 27, 8, 0, 0), symptom_id=2, severity=3)

    # Add a user symptom ingredient link
    user_symptom_ingredient_link_1 = UserSymptomIngredientLink(id=1, user_id=1,
                                    symptom_id=2, ingredient_id=7)
    
    db.session.add_all([symptom_log_1, food_ingrd_1, food_ingrd_2, food_ingrd_3, 
                        food_ingrd_4, food_ingrd_5, food_ingrd_6, food_ingrd_7, 
                        food_log_1, user_symptom_ingredient_link_1,
                        ])

    db.session.commit()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    init_app()

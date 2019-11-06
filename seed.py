import datetime
from sqlalchemy import func

from model import db, connect_to_db, User, Food, FoodIngredient, Ingredient, Symptom, SymptomLog, FoodLog, UserSymptomFoodLink
from server import app

def load_users():
    """Load fake users into database"""

    User.query.delete()

    print('Adding users...')

    user_1 = User(email='john@doe.com', password='fluffy89')
    user_2 = User(email='jane@doe.com', password='secure-password')
    user_3 = User(email='kelly@banana.com', password='password123')

    db.session.add_all([user_1, user_2, user_3])

    db.session.commit()

    print('Users added!')


def load_symptoms():
    """Add smyptoms into the database"""

    Symptom.query.delete()

    print('Adding symptoms...')

    symp_1 = Symptom(name='heartburn')
    symp_2 = Symptom(name='migrain')
    symp_3 = Symptom(name='nausea')
    symp_4 = Symptom(name='indigestion')
    symp_5 = Symptom(name='upset stomach')

    db.session.add_all([symp_1, symp_2, symp_3, symp_4, symp_5])

    db.session.commit()

    print('Symptoms added!')


def load_foods():
    """Add some foods into the database"""

    Food.query.delete()

    print('Adding foods...')

    food_1 = Food(name='Kraft Macaroni And Cheese Dinner', brand_name='Kraft')
    # nix_item_id = 51d2ff1dcc9bff111580f5e4

    db.session.add(food_1)

    db.session.commit()

def load_ingredients():

    Ingredient.query.delete()

    print('Adding ingredients...')

    ingrd_1 = Ingredient(name='wheat flour')
    ingrd_2 = Ingredient(name='niacin')
    ingrd_3 = Ingredient(name='milkfat')
    ingrd_4 = Ingredient(name='salt')
    ingrd_5 = Ingredient(name='whey')

    db.session.add_all([ingrd_1, ingrd_2, ingrd_3, ingrd_4, ingrd_5])

    db.session.commit()

def load_food_ingredients():

    FoodIngredient.query.delete()

    print('Adding food ingredients...')

    food_ingr_1 = FoodIngredient(food_id=1, ingredient_id=1)
    food_ingr_2 = FoodIngredient(food_id=1, ingredient_id=2)
    food_ingr_3 = FoodIngredient(food_id=1, ingredient_id=3)
    food_ingr_4 = FoodIngredient(food_id=1, ingredient_id=4)
    food_ingr_5 = FoodIngredient(food_id=1, ingredient_id=5)

    db.session.add_all([food_ingr_1, food_ingr_2, food_ingr_3, food_ingr_4, food_ingr_5])

    db.session.commit()








if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_symptoms()
    load_foods()
    load_ingredients()
    load_food_ingredients()
    print('All done!')
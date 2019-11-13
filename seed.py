from datetime import datetime

from model import (db, connect_to_db, User, Symptom, Meal)
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
    symp_2 = Symptom(name='migraine')
    symp_3 = Symptom(name='nausea')
    symp_4 = Symptom(name='indigestion')
    symp_5 = Symptom(name='upset stomach')

    db.session.add_all([symp_1, symp_2, symp_3, symp_4, symp_5])

    db.session.commit()

    print('Symptoms added!')


# def load_foods():
#     """Add some foods into the database"""

#     Food.query.delete()

#     print('Adding foods...')

#     food_1 = Food(name='Kraft Macaroni And Cheese Dinner', brand_name='Kraft')
#     food_2 = Food(name='Pumpkin Chia Pudding', brand_name='Thistle')
#     # nix_item_id = 51d2ff1dcc9bff111580f5e4

#     db.session.add_all([food_1, food_2])

#     db.session.commit()

# def load_ingredients():

#     Ingredient.query.delete()

#     print('Adding ingredients...')

#     ingrd_1 = Ingredient(name='wheat flour')
#     ingrd_2 = Ingredient(name='niacin')
#     ingrd_3 = Ingredient(name='milkfat')
#     ingrd_4 = Ingredient(name='salt')
#     ingrd_5 = Ingredient(name='whey')
#     ingrd_6 = Ingredient(name='hemp milk')
#     ingrd_7 = Ingredient(name='pumkin')
#     ingrd_8 = Ingredient(name='banana')
#     ingrd_9 = Ingredient(name='maple syrup')
#     ingrd_10 = Ingredient(name='chia seeds')
#     ingrd_11 = Ingredient(name='pea protein powder')
#     ingrd_12 = Ingredient(name='orange zest')

#     db.session.add_all([ingrd_1, ingrd_2, ingrd_3, ingrd_4, ingrd_5,    
#                         ingrd_6, ingrd_7, ingrd_8, ingrd_9, ingrd_10, ingrd_11,
#                         ingrd_12])

#     db.session.commit()

# def load_food_ingredients():

#     FoodIngredient.query.delete()

#     print('Adding food ingredients...')

#     food_ingrd_1 = FoodIngredient(food_id=1, ingredient_id=1)
#     food_ingrd_2 = FoodIngredient(food_id=1, ingredient_id=2)
#     food_ingrd_3 = FoodIngredient(food_id=1, ingredient_id=3)
#     food_ingrd_4 = FoodIngredient(food_id=1, ingredient_id=4)
#     food_ingrd_5 = FoodIngredient(food_id=1, ingredient_id=5)
#     food_ingrd_6 = FoodIngredient(food_id=2, ingredient_id=6)
#     food_ingrd_7 = FoodIngredient(food_id=2, ingredient_id=7)
#     food_ingrd_8 = FoodIngredient(food_id=2, ingredient_id=8)
#     food_ingrd_9 = FoodIngredient(food_id=2, ingredient_id=9)
#     food_ingrd_10 = FoodIngredient(food_id=2, ingredient_id=10)
#     food_ingrd_11 = FoodIngredient(food_id=2, ingredient_id=11)
#     food_ingrd_12 = FoodIngredient(food_id=2, ingredient_id=12)

#     db.session.add_all([food_ingrd_1, food_ingrd_2, food_ingrd_3, food_ingrd_4, 
#                         food_ingrd_5, food_ingrd_6, food_ingrd_7, food_ingrd_8,
#                         food_ingrd_9, food_ingrd_10, food_ingrd_11, food_ingrd_12])

#     db.session.commit()

def load_meals():

    meal_1 = Meal(name='breakfast')
    meal_2 = Meal(name='lunch')
    meal_3 = Meal(name='dinner')
    meal_4 = Meal(name='snacks')

    db.session.add_all([meal_1, meal_2, meal_3, meal_4])
    db.session.commit()

# def load_food_logs():

#     FoodLog.query.delete()

#     print('Adding food logs...')

#     food_log_1 = FoodLog(ts=datetime.now(), meal_id=2, user_id=1, food_id=1)
#     food_log_2 = FoodLog(ts=datetime.now(), meal_id=1, user_id=1, food_id=2)

#     db.session.add_all([food_log_1, food_log_2])

#     db.session.commit()

def find_common_ingredients(ingredient_lists_list):
    """Takes in a list of ingredient lists and returns the ingredients 
    in common between (2+ occurences) lists within a dictionary"""

    all_ingredients = {}
    common_ingredients = {}

    for ingredient_list in ingredient_lists_list:
        for ingredient in ingredient_list:
            all_ingredients[ingredient] = all_ingredients.get(ingredient, 0) + 1

    for ingredient, count in all_ingredients.items():
        if count > 1:
            common_ingredients[ingredient] = count

    return common_ingredients


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # load_users()
    # load_symptoms()
    # load_foods()
    # load_ingredients()
    # load_food_ingredients()
    # load_meals()
    # load_food_logs()

    print('All done!')
import datetime
from sqlalchemy import func

from model import db, connect_to_db, User, Food, FoodIngredient, Ingredient, Symptom, SymptomLog, FoodLog, UserSymptomFoodLink
from server import app

def load_users():
    """Load fake users into database"""

    print('Adding users...')

    user_1 = User(email='john@doe.com', password='fluffy89')
    user_2 = User(email='jane@doe.com', password='secure-password')
    user_3 = User(email='kelly@banana.com', password='password123')

    db.session.add_all([user_1, user_2, user_3])

    db.session.commit()

    print('Users added!')


def load_symptoms():
    """Add smyptoms into the database"""

    print('Adding symptoms...')

    heartburn = Symptom(name='heartburn')
    migrain = Symptom(name='migrain')
    nausea = Symptom(name='nausea')
    indigestion = Symtpom(name='indigestion')
    upset_stomach = Symptom(name='upset_stomach')

    db.session.add_all([hearburn, migrain, indigestion, upset_stomach])

    db.session.commit()

    print('Symptoms added!')






if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_symptoms()
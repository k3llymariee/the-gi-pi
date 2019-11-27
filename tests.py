import unittest
from server import app
from model import (db, connect_to_db, User, Food, FoodIngredient, Ingredient, 
    Symptom, SymptomLog, FoodLog, UserSymptomIngredientLink, Meal, example_data,
    init_app)
from flask import session

class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    # def test_ingredients_list(self):
    #     """Test the ingredients list"""

    #     result = self.client.get("/api/symptoms")
    #     print(result.data)
    #     self.assertIn(b"heartburn", result.data)
        # TO DO check to see if it's json

class FlaskTestsLoggedIn(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'most-secret'
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

        # TODO: NEED TO ADD CONNECT TO DB

    def test_home_page(self):
        """Test important page."""

        result = self.client.get("/2019-11-26")
        self.assertIn(b"Your food diary for", result.data)


if __name__ == "__main__":

    unittest.main()
    init_app()
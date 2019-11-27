from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_ingredients_list(self):
        """Test the ingredients list"""

        result = self.client.get("/ingredients")
        self.assertIn(b"pumpkin", result.data)

class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'most-secret'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_home_page(self):
        """Test important page."""

        result = self.client.get("/2019-11-26")
        self.assertIn(b"Your food diary for", result.data)
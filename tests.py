import unittest
from server import app
from model import *
from flask import session

class FlaskTestsMain(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'most-secret'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


class FlaskTestsLogInLogOut(unittest.TestCase):
    """Flask tests with DB but user not logged in (yet)"""

    def setUp(self):
        """Stuff to do before every test."""

        # Set up the Flask test client
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'most-secret'
        self.client = app.test_client()

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

    def test_process_login(self):
        """Test if an existing user is able to log in"""

        result = self.client.post('/login',
                                  data={
                                    'email': 'john@doe.com', 
                                    'password': 'fluffy89',
                                  },
                                  follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<p>Here would be a daily view of:</p>', result.data)



if __name__ == "__main__":

    unittest.main()
    init_app()
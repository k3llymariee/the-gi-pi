import unittest
from server import app
from model import *
from flask import session, flash
from datetime import date
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

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

        # self.browser = webdriver.Chrome()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

        # self.browser.quit()


    def test_logged_in_index(self):
        """Testing the logged in redirect from home page process"""

        result = self.client.get("/", follow_redirects=True)
        self.assertIn(b"Your food diary for", result.data)


    def test_logout(self):
        """Test if the logout process removes the user_id in the flask session"""

        result = self.client.get("/logout", follow_redirects=True)

        with self.client.session_transaction() as session:
            session_user = dict(session).get('user_id')
        
        self.assertEqual(result.status_code, 200)
        self.assertIsNone(session_user)

    # def test_daily_view(self):
    #     """Test if the daily view properly displays food logs and symptom logs"""

    #     food_log = FoodLog.query.get(1)
    #     selected_date = (food_log.ts).strftime('%Y-%m-%d')

    #     result = self.client.get(f'/{selected_date}')
    #     # print('RESULT', result.data)
        
    #     print('FOOD LOG', food_log)

    #     self.assertIn(b'Pumpkin', result.data)


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


    def test_logged_out_index(self):
        """Testing the logged out redirect from home page process"""

        result = self.client.get("/", follow_redirects=True)
        self.assertIn(b"Confirm Password", result.data)


    def test_process_login(self):
        """Test if an existing user is able to log in successfully"""

        result = self.client.post('/login',
                                          data={
                                            'email': 'john@doe.com', 
                                            'password': 'fluffy89',
                                          },
                                          follow_redirects=True,
                                 )

        pre_redirect = self.client.post('/login',
                                          data={
                                            'email': 'john@doe.com', 
                                            'password': 'fluffy89',
                                          },
                                       )

        with self.client.session_transaction() as session:
            session_user = dict(session).get('user_id')
            flash_message = session.get('_flashes')

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<p>Here would be a daily view of:</p>', result.data)
        self.assertIsNotNone(session_user)
        self.assertEqual(flash_message[0][1], 'Successfully logged in')

    def test_process_login_incorrect_password(self):
        """Test if the correct flash message appears for an incorrect password"""

        result = self.client.post('/login',
                                        data={
                                            'email': 'john@doe.com', 
                                            'password': 'incorrect',
                                        },
                                        # follow_redirects=True,
                                        )
        
        with self.client.session_transaction() as session:
            flash_message = session.get('_flashes')

        post_redirect = self.client.post('/login',
                                        data={
                                            'email': 'john@doe.com', 
                                            'password': 'incorrect',
                                        },
                                        follow_redirects=True,
                                        )
        
        self.assertEqual(result.status_code, 302)
        self.assertIsNotNone(flash_message, session['_flashes'])
        self.assertEqual(flash_message[0][1], 'Incorrect password or email')
        self.assertEqual(post_redirect.status_code, 200)
        self.assertIn(b'<h1>User login</h1>', post_redirect.data)

    def test_process_login_incorrect_email(self):
        """Test if the correct flash message appears for an incorrect email"""

        result = self.client.post('/login',
                                        data={
                                            'email': 'john@dont.com', 
                                            'password': 'fluffy89',
                                        },
                                        # follow_redirects=True,
                                        )
        
        with self.client.session_transaction() as session:
            flash_message = session.get('_flashes')

        post_redirect = self.client.post('/login',
                                        data={
                                            'email': 'john@doe.com', 
                                            'password': 'incorrect',
                                        },
                                        follow_redirects=True,
                                        )

        # Assert
        self.assertEqual(result.status_code, 302)
        self.assertIsNotNone(flash_message, session['_flashes'])
        self.assertEqual(flash_message[0][1], 'Incorrect email or password')
        self.assertEqual(post_redirect.status_code, 200)
        self.assertIn(b'<h1>User login</h1>', post_redirect.data)

class TestDailyView(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # selenium stuff
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        # print("Set-up for testing completed")


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

        self.browser.quit()

    def test_daily_view(self):
        
        food_log = FoodLog.query.get(1)
        selected_date = (food_log.ts).strftime('%Y-%m-%d')

        result = self.browser.get(f'http://localhost:5000/{selected_date}')

        print('RESULT:', result.data)

            # download geckdriver, put it in path (see stackoverflow)

        
        

if __name__ == "__main__":

    unittest.main()
    init_app()
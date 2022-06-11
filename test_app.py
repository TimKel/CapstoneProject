import os, io
from unittest import TestCase
from sqlalchemy import exc
from flask import session
from models import db, connect_db, User, Skatepark 

os.environ['DATABASE_URL'] = "postgresql:///skateparks_test"

from app import app, CURR_USER_KEY, APIkey
db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class UserLoginAndSignUpTesting(TestCase):
    """Tests routes for user authenication/authorization/signup/login functionality"""

    def setUp(self):
        """Create test client, add sample data"""

        User.query.delete()

        self.client = app.test_client()

        #Create test users
        self.test_user = User.signup(
                                    username='testuser',
                                    email='testuser1@test.com',
                                    password='testing1',
                                    location= 'test1',
                                    image_url= None,)

        db.session.commit()

    

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_home(self):
        """Test that user is redirected to correct place based on login status"""

        #If user logged in, redirect to '/' with main search page
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id

            resp=c.get('/', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Search Parks', str(resp.data))
        
        #If user not logged in, re-render template for Log In
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = None

            resp=c.get('/users/login')
            self.assertEqual(resp.status_code, 404)
            self.assertIn('Not Found', str(resp.data))

    def test_signup(self):
        """Test that logged in user can register a new account or declined if they 
        already have an account or username has been taken"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id

            resp=c.get('/signup', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Search Parks", str(resp.data))

    def test_logout(self):
        """Test that log out route successfully logs out with a flash message"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id

            resp=c.get('/logout', follow_redirects=True)
            self.assertIn("succesfully signed out", str(resp.data))

    def test_edit_profile(self):
        """Does the form render"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id

            resp=c.get('/users/profile')
            html = resp.get_data(as_text=True)

            # Does the edit form page render
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Your Profile', str(resp.data))
            self.assertIn('To confirm changes, enter your password', str(resp.data))

            



class SearchViewFunctionsTesting(TestCase):
    """Test search view functions that handle API's and return templates displaying data via params"""

    def setUp(self):
        """Create test client, add sample data"""

        Skatepark.query.delete()

        self.client = app.test_client()

        #Create test users
        self.test_park = Skatepark(
                                    name='Mcdowell Skatepark',
                                    address='15525 N Thompson Peak Pkwy Scottsdale AZ',
                                    description='The park features a bowl',
                                    image_url= None,)
        db.session.add(self.test_park)
        db.session.commit()

    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp


    def test_homepage(self):
        """Tests render of homepage"""
        with app.test_client() as c:
            resp=c.get('/')
            self.assertEqual(resp.status_code, 200)

    def test_search_parks(self):
        """Tests render of homepage"""
        with app.test_client() as c:
            resp=c.get('/search')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Mcdowell', str(resp.data))

    def test_search_area(self):
        """Tests specific location"""
        with app.test_client() as c:
            resp=c.get('/search')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('AZ', str(resp.data))

# Originally a test for map population but it showed my API key so I deleted it

    def test_login_form(self):
        """Tests specific location"""
        with app.test_client() as c:
            resp=c.get('/login')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Welcome back', str(resp.data))

    def test_signup_form(self):
        """Tests specific location"""
        with app.test_client() as c:
            resp=c.get('/signup')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username', str(resp.data))
            self.assertIn('E-mail', str(resp.data))
            self.assertIn('Profile Image', str(resp.data))
            self.assertIn('Location', str(resp.data))
            self.assertIn('Password', str(resp.data))

    

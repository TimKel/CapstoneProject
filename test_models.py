import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Skatepark

os.environ['DATABASE_URL'] = "postgresql:///skateparks_test"

from app import app


db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com", "password", None, "Las Vegas")
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "password", None, "Arizona")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            location="somewhere",
            image_url=None
        )

        db.session.add(u)
        db.session.commit()

        # Basic info is accurate
        self.assertEqual(1, u.id)
        self.assertEqual('testuser', u.username)
        self.assertEqual('somewhere', u.location)

    
    # Signup Tests
    #
    ####
    def test_valid_signup(self):
        u_test = User.signup("testtesttest", "testtest@test.com", "password", None, "somewhere")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertNotEqual(u_test.password, "password")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "test@test.com", "password", None, None)
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("testtest", None, "password", None, None)
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "", None, None)
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", None, None, None)
    
    ###
    
    # Authentication Tests
    
    ###
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))

class SkateparkModelTestCase(TestCase):
    """Test model for Skatepark."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        park1 = Skatepark(name='Mcdowell Skatepark',
                            address='15525 N Thompson Peak Pkwy Scottsdale AZ',
                            description='The park features a bowl',
                            image_url= None)

        park2 = Skatepark(name='Metro',
                            address='3509 N Sweden St, Las Vegas, NV 89129',
                            description='The street section consists of a variety of stair sets',
                            image_url= None)
        
        db.session.add_all([park1, park2])
        db.session.commit()
        self.client = app.test_client()


    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_model(self):
        """Does basic model work?"""

        s = Skatepark(
            name='Test Skatepark',
            address='1234 Testing Address',
            image_url= None,
            description='The park features a bowl. Full of tests'
        )

        db.session.add(s)
        db.session.commit()

        # Basic info is accurate
        self.assertEqual(3, s.id)
        self.assertEqual('Test Skatepark', s.name)
        self.assertEqual('1234 Testing Address', s.address)

    # Test for invalid park additions

    def test_invalid_name(self):
        invalid = Skatepark(
            name= None,
            address='1234 Testing Address',
            description='The park features a bowl. Full of tests',
            image_url= None)
        pid = 123456789
        invalid.id = pid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_address(self):
        invalid = Skatepark(
            name= 'Test Skatepark',
            address= None,
            description='The park features a bowl. Full of tests',
            image_url= None)
        pid = 123789
        invalid.id = pid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.add(invalid)
            db.session.commit()
    
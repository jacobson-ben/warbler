"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        u1 = User.signup("Benny", "testing11@gmail.com", "testing", None)
        u1.id = 1000

        u2 = User.signup("Zacky", "testing12@gmail.com", "testing", None)
        u2.id = 2000

        u3 = User.signup("Johnathan", "testing13@gmail.com", "testing", None)
        u3.id = 3000

        db.session.commit()

        self.u1 = u1
        self.u2 = u2
        self.u3 = u3


    def tearDown(self):
        
        db.session.rollback()


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    
    def test_repr(self):
        """Does the repr work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(repr(u), f"<User #{u.id}: testuser, test@test.com>")
    
    
    def test_following(self):

        self.u1.following.append(self.u2)
        db.session.commit()
        self.assertIn(self.u2, self.u1.following)
        self.assertEqual(len(self.u1.following), 1)
        
        self.u1.following.append(self.u3)
        db.session.commit()
        self.assertEqual(len(self.u1.following), 2)

        self.u1.following.remove(self.u2)
        db.session.commit()
        self.assertNotIn(self.u2, self.u1.following)
        self.assertEqual(len(self.u1.following), 1)

    
    def test_followers(self):

        self.u1.followers.append(self.u2)
        db.session.commit()
        self.assertIn(self.u2, self.u1.followers)
        self.assertEqual(len(self.u1.followers), 1)

        self.u1.followers.remove(self.u2)
        db.session.commit()
        self.assertNotIn(self.u2, self.u1.followers)
        self.assertEqual(len(self.u1.followers), 0)

    
    def test_signup(self):
        
        test_user = User.signup("Teddy", "testing20@gmail.com", "testing", "")
        test_user.id = 4000
        db.session.add(test_user)
        db.session.commit()

        user = User.query.get_or_404(test_user.id)

        self.assertEqual(user.id, 4000)
        self.assertEqual(user.username, "Teddy")

    
    def test_signup_fail(self):
        
        test_user = User.signup("T", None, "testing", None)
        with self.assertRaises(exc.IntegrityError): 
            db.session.commit()

    
    def test_valid_authentication(self):

        usr = User.authenticate(self.u1.username, "testing")
        self.assertIsNotNone(usr)
        self.assertEqual(usr.id, self.u1.id)
        

        


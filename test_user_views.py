"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py

import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()
    
        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        
        self.u1 = User.signup("Benny", "testing11@gmail.com", "testing", None)
        self.u1.id = 1000

        self.u2 = User.signup("Zacky", "testing12@gmail.com", "testing", None)
        self.u2.id = 2000

        self.u3 = User.signup("Johnathan", "testing13@gmail.com", "testing", None)
        self.u3.id = 3000

        db.session.commit()
    
    def tearDown(self):
        db.session.rollback()
    
    def test_view_following(self):
        """Can use add a message?"""

        self.u1.following.append(self.u2)
        db.session.commit()

        self.u1 = User.query.get(1000)
        self.u2 = User.query.get(2000)

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            
            resp = c.get(f"/users/{self.u1.id}/following")
            html = resp.get_data(as_text=True)

            #tests that a logged in user can view a user's following page
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<p>@{self.u2.username}</p>", html)
        
    def logged_out_user_following(self):
        resp = self.client.get(f"/users/1/following")

        #tests that a logged out user can view a user's following page
        self.assertEqual(resp.status_code, 404)

    

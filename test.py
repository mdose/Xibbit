import unittest

from server import app
from model import db, connect_to_db
from seed import load_art_types, load_collections, load_art_movements
from seed import load_subject_matters, load_artists, load_art
from seed import load_users, set_val_user_id

# class TestCase(TestCase):

#     def test_func(self):
#         self.assert


def load_seed_data():
    """Loads seed data into testdb"""
# TODO: works for now with small seed, but if seed.py grows bigger, create a small testdb
# so that tests don't take forever to run!!!

    load_art_types()
    load_collections()
    load_art_movements()
    load_subject_matters()
    load_artists()
    load_art()
    load_users()
    set_val_user_id()


class FlaskTest(unittest.TestCase):

    def setUp(self):
        """Things to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "IDKAnythingreally"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        load_seed_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = 1

    def tearDown(self):
        """Things to do after every test."""
        db.session.close()
        db.drop_all()

    def test_show_homepage(self):
        """Tests the homepage route"""
        result = self.client.get("/")
        self.assertIn("Search for Art", result.data)

    def test_no_registration_yet(self):
        """Tests the /register GET route"""
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Please register here", result.data)

    def test_registration_process(self):
        """Tests the /register POST route"""
        result = self.client.post("/register",
                                  data={"username": "hi",
                                        "password": "hi",
                                        "email": "hi@hi.com"},
                                  follow_redirects=True)
        self.assertNotIn("Please register here", result.data)

    def test_no_login_yet(self):
        """Tests the /login GET route"""
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Login here", result.data)

    def test_login_process(self):
        """Tests the /login POST route"""
        result = self.client.post("/login",
                                  data={"password": "hi",
                                        "email": "hi@hi.com"},
                                  follow_redirects=True)
        self.assertNotIn("Login here", result.data)

    def test_logout(self):
        """Tests the /logout route"""
    # FIXME: Figure out how to make this work. (It has sessions)
        
        result = self.client.get('/logout')
        self.assertEqual(result.status_code, 200)
        self.assertIn("You are now logged out.", result.data)

    def test_show_user(self):
        """Tests the "/users/<user_id>"route."""

        result = self.client.get('/users/2')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Profile", result.data)

    def test_show_art(self):
        """Tests the "/artworks/<art_id>" route"""

        result = self.client.get('/artworks/2')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Title", result.data)

    def test_show_artist(self):
        """Tests the "/artists/<artist_id>" route"""

        result = self.client.get('/artists/2')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Lifespan", result.data)

    def test_show_collection(self):
        """Tests the "/collections/<collection_id>" route"""

        result = self.client.get('collections/2')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Location", result.data)

if __name__ == "__main__":
    unittest.main()

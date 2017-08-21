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
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        load_seed_data()

    def tearDown(self):
        """Things to do after every test."""
        db.session.close()
        db.drop_all()

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Search for Art", result.data)

    def test_no_registeration_yet(self):
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Please register here", result.data)

    def test_registration(self):
        result = self.client.post("/register",
                                  data={"username": "hi",
                                        "password": "hi",
                                        "email": "hi@hi.com"},
                                  follow_redirects=True)
        self.assertNotIn("Please register here", result.data)


if __name__ == "__main__":
    unittest.main()

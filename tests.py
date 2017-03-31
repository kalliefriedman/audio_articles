import unittest

from server import app
from model import db, example_data, connect_to_db


# class HomepageTests(unittest.TestCase):
#     """Tests for my party site."""

#     def setUp(self):
#         self.client = app.test_client()
#         app.config['TESTING'] = True

#     def test_homepage(self):
#         result = self.client.get("/")
#         self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

#     def test_no_rsvp_yet(self):
#         # FIXME: Add a test to show we see the RSVP form, but NOT the
#         # party details
#         result = self.client.get("/")
#         self.assertNotIn("Party Details", result.data)
#         self.assertIn("RSVP", result.data)

#     def test_rsvp(self):
#         result = self.client.post("/rsvp",
#                                   data={"name": "Jane",
#                                         "email": "jane@jane.com"},
#                                   follow_redirects=True)
#         # FIXME: Once we RSVP, we should see the party details, but
#         # not the RSVP form
#         self.assertIn("Party Details", result.data)
#         self.assertNotIn("RSVP", result.data)


class AudioArticlesTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """What needs to be done prior to each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # with self.client as c:
        #     with c.session_transaction() as sess:
        #         sess[''] = True

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_backrefs(self):
        # Test that backrefs work from example_data()
        result = self.client.get("/games", data={'session["RSVP"]': True})
        self.assertIn("Clue", result.data)


if __name__ == "__main__":
    unittest.main()

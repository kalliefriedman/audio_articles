import unittest

from flask import (Flask, Response, render_template, redirect, request, flash,
                   session, jsonify)
import unittest

from server import app
from model import db, connect_to_db, example_data_users, example_data_articles, example_data_tags, example_data_taggings


class TestLoggedOut(unittest.TestCase):
    """Tests for audio articles site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        if "user_id" in session:
            del session["user_id"]

    def test_homepage(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Audio Articles", result.data)

    def test_register(self):
        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Name", result.data)

    def test_register_process(self):
        result = self.client.post("/register-process",
                                  data={'username': "kallies",
                                        'f_name': "kallie",
                                        'l_name': "l_name",
                                        'password': "password",
                                        'email': "kallies@yahoo.com",
                                        'password_salt': ""},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 302)

    def test_login(self):
        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Login", result.data)

    def test_login_process(self):
        result = self.client.post("/login-process",
                                  data={"username_or_email": 'kallies@yahoo.com', "password": "password"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 302)

    def test_logout(self):
        result = self.client.post("/logout",
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 302)

    def test_create_article(self):
        result = self.client.get("/create-article")
        self.assertEqual(result.status_code, 302)

    def test_user_articles(self):
        user_id = 1
        result = self.client.get("/user-articles/" + user_id)
        self.assertEqual(result.status_code, 302)

    def test_article_add_process(self):
        result = self.client.post("/article-add-process",
                                  data={'article_title': "sample title",
                                        "user_id": '1',
                                        'article_text': 'all the article text'},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 302)

    def test_article_closeup(self):
        article_id = 1
        result = self.client.get("/article-closeup/" + article_id)
        self.assertEqual(result.status_code, 302)

    def test_article_edit(self):
        article_id = 1
        result = self.client.get("/article-edit/" + article_id)
        self.assertEqual(result.status_code, 302)

    def test_read(self):
        result = self.client.get("/read")
        self.assertEqual(result.status_code, 302)


# class LoggedInHomepageTests(unittest.TestCase):
#     """Testing logged in version of homepage"""

#     def setUp(self):
#         self.client = app.test_client()
#         app.config['TESTING'] = True
#         session["user_id"] = 1

#     def tearDown(self):
#         """Do at end of every test."""
#         del session["user_id"]

#     def test_logged_in(self):
#         result = self.client.get("/",
#                                  follow_redirects=True)
#         self.assertIn("Add Article", result.data)


# class AudioArticlesTestsDatabase(unittest.TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """What needs to be done prior to each test."""

#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         # Connect to test database (uncomment when testing database)
#         connect_to_db(app, "postgresql:///testdb")

#         # with self.client as c:
#         #     with c.session_transaction() as sess:
#         #         sess[''] = True

#         # Create tables and add sample data (uncomment when testing database)
#         db.create_all()
#         example_data()

#     def tearDown(self):
#         """Do at end of every test."""

#         # (uncomment when testing database)
#         db.session.close()
#         db.drop_all()

#     def test_backrefs(self):
#         # Test that backrefs work from example_data()
#         result = self.client.get("/games", data={'session["RSVP"]': True})
#         self.assertIn("Clue", result.data)


if __name__ == "__main__":
    unittest.main()

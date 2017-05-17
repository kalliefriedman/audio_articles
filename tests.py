from flask import (Flask, Response, render_template, redirect, request, flash,
                   session, jsonify)
import unittest
from server import app, session
from model import db, connect_to_db, example_data_users, example_data_articles, example_data_tags, example_data_taggings


class TestLoggedOut(unittest.TestCase):
    """Tests for audio articles site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()

    def tearDown(self):
        """Should close the session and drop all tables"""
        db.session.close()
        db.drop_all()

    def testHomepage(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome to Audio Articles")

    def testRegister(self):
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Register")

    def testLogin(self):
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Login")

    def testCreateArticle(self):
        result = self.client.get('/create-article')
        self.assertEqual(result.status_code, 302)
        self.assertIn("Login")

    def testUserArticles(self):
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()
        result = self.client.get('/user-articles/1')
        self.assertEqual(result.status_code, 302)
        self.assertIn("Login")

    def testArticleCloseup(self):
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()
        result = self.client.get('/article-closeup/1')
        self.assertEqual(result.status_code, 302)
        self.assertIn("Login")

    def testArticleEdit(self):
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()
        result = self.client.get('/article-edit/1')
        self.assertEqual(result.status_code, 302)
        self.assertIn("Login")

    def testRead(self):
        result = self.client.get('/read', data={'text': "Hi this is a test",
                                                'voice_id': "Amy",
                                                'article_id': "1"})
        self.assertEqual(result.status_code, 302)


class TestLoggedIn(unittest.TestCase):
    """Testing logged in version of homepage"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

    def tearDown(self):
        """Should close the session and drop all tables"""
        db.session.close()
        db.drop_all()

    def testHomepage(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 302)
        self.assertIn("Welcome,")

    def testRegister(self):
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 302)
        self.assertIn("Welcome,")

    def testLogin(self):
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 302)
        self.assertIn("Welcome,")

    def testCreateArticle(self):
        result = self.client.get('/create-article', query_string={'user_id_from_form': "1"})
        self.assertEqual(result.status_code, 200)
        self.assertIn("Title:")

    def testUserArticles(self):
        result = self.client.get('/user-articles/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome")

    def testArticleCloseup(self):
        result = self.client.get('/article-closeup/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Select a voice:")

    def testArticleEdit(self):
        result = self.client.get('/article-edit/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Title:")

    def testRead(self):
        result = self.client.get('/read', query_string={'text': "Hi this is a test",
                                                        'voice': "Amy",
                                                        'article_id': "1"})
        self.assertEqual(result.status_code, 200)

    def testRegisterProcess(self):
        result = self.client.post('/register-process',
                                  data={'username': "kallies",
                                        'f_name': "kallie",
                                        'l_name': "l_name",
                                        'password': "password",
                                        'email': "kallies@yahoo.com",
                                        'password_salt': ""},
                                  )
        self.assertEqual(result.status_code, 302)
        self.assertIn("Welcome,")

    def testArticleAddProcess(self):
        result = self.client.post('/article-add-process',
                                  data={'article_title': "sample title",
                                        "user_id": '1',
                                        'article_text': 'all the article text'},
                                  )
        self.assertEqual(result.status_code, 302)

    def testLoginProcess(self):
        result = self.client.post('/login-process',
                                  data={"username_or_email": 'kallies@yahoo.com', "password": "password"},
                                  )
        self.assertEqual(result.status_code, 302)
        self.assertIn("Welcome,")

    def testTagAddProcess(self):
        result = self.client.post('/tag-add-process.json', data={"tag_value": "sample tag", "article_id": "1", "user_id_value": "1"})
        self.assertEqual(result.status_code, 200)
        self.assertIn("Title:")


    def testFilterArticlesByTag(self):
        result = self.client.get('/filter-articles/Recent')
        self.assertEqual(result.status_code, 200)

    def testDeleteArticle(self):
        result = self.client.post('/delete-article/3')
        self.assertEqual(result.status_code, 302)

    def testDeleteTag(self):
        result = self.client.post('/delete-tag', data={"tag_id": "1", "article_id": "1"})
        self.assertEqual(result.status_code, 200)

    def testUserProfile(self):
        result = self.client.get('/user-profile')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Username:")

# need to test everything from here down for logic and syntax
class TestDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """What needs to be done prior to each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        db.drop_all()

    def testUsersData(self):
        """Testing user data format is correct"""
        result = self.client.get("/games")
        self.assertIn("Power Grid", result.data)

    def testArticlesData(self):
        """Testing article data format is correct"""
        result = self.client.get("/user_articles/1")
        self.assertIn("Kallie", result.data)

    def testTagsData(self):
        """Testing tags data format is correct"""
        result = self.client.get("/user_articles/1")
        self.assertIn("Recent", result.data)

if __name__ == "__main__":
    unittest.main()

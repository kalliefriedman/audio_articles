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
        result = self.client.get('/', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome to Audio Articles", result.data)

    def testRegister(self):
        result = self.client.get('/register', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Register", result.data)

    def testLogin(self):
        result = self.client.get('/login', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Login", result.data)

    def testCreateArticle(self):
        result = self.client.get('/create-article', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Login", result.data)

    def testUserArticles(self):
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()
        result = self.client.get('/user-articles/1', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Login", result.data)

    def testArticleCloseup(self):
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()
        result = self.client.get('/article-closeup/1', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Login", result.data)

    def testArticleEdit(self):
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()
        result = self.client.get('/article-edit/1', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Login", result.data)

    def testRead(self):
        result = self.client.get('/read', data={'text': "Hi this is a test",
                                                'voice_id': "Amy",
                                                'article_id': "1"}, follow_redirects=True)
        self.assertEqual(result.status_code, 200)


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
        result = self.client.get('/', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome,", result.data)

    def testRegister(self):
        result = self.client.get('/register', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome,", result.data)

    def testLogin(self):
        result = self.client.get('/login', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome,", result.data)

    def testCreateArticle(self):
        result = self.client.get('/create-article',
                                 query_string={'user_id_from_form': "1"}, 
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Title:", result.data)

    def testUserArticles(self):
        result = self.client.get('/user-articles/1', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome", result.data)

    def testArticleCloseup(self):
        result = self.client.get('/article-closeup/1', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Select a voice:", result.data)

    def testArticleEdit(self):
        result = self.client.get('/article-edit/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Title:", result.data)

    def testRead(self):
        result = self.client.get('/read', query_string={'text': "Hi this is a test",
                                                        'voice': "Amy",
                                                        'article_id': "1"}, 
                                                        follow_redirects=True)
        self.assertEqual(result.status_code, 200)

    def testRegisterProcess(self):
        result = self.client.post('/register-process',
                                  data={'username': "kallies",
                                        'f_name': "kallie",
                                        'l_name': "l_name",
                                        'password': "password",
                                        'email': "kallies@yahoo.com",
                                        'password_salt': ""},
                                        follow_redirects=True
                                  )
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome,", result.data)

    def testArticleAddProcess(self):
        result = self.client.post('/article-add-process',
                                  data={'article_title': "sample title",
                                        "user_id": '1',
                                        'article_text': 'all the article text'}, 
                                        follow_redirects=True,
                                  )
        self.assertEqual(result.status_code, 200)

    def testLoginProcess(self):
        result = self.client.post('/login-process',
                                  data={"username_or_email": 'kallies@yahoo.com', "password": "password"}, 
                                  follow_redirects=True
                                  )
        self.assertEqual(result.status_code, 200)
        self.assertIn("Welcome,", result.data)

    def testTagAddProcess(self):
        result = self.client.post('/tag-add-process.json', 
            data={"tag_value": "sample tag", "article_id": "1", "user_id_value": "1"}, 
            follow_redirects=True)
        self.assertEqual(result.status_code, 200)

    def testFilterArticlesByTag(self):
        result = self.client.get('/filter-articles/Recent', follow_redirects=True)
        self.assertEqual(result.status_code, 200)

    def testDeleteArticle(self):
        result = self.client.post('/delete-article/3', follow_redirects=True)
        self.assertEqual(result.status_code, 200)

    def testDeleteTag(self):
        result = self.client.post('/delete-tag', data={"tag_id": "1", "article_id": "1"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)

    # need to fix react rendering on this page
    # def testUserProfile(self):
    #     result = self.client.get('/user-profile')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn("Username:", result.data)


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

    # def testArticlesData(self):
    #     """Testing user data format is correct"""
    #     result = self.client.get("/user_articles/1", follow_redirects=True)
    #     self.assertIn("Myers Briggs History", result.data)

    # def testUsersData(self):
    #     """Testing article data format is correct"""
    #     result = self.client.get("/user_articles/1", follow_redirects=True)
    #     self.assertIn("Kallie", result.data)

    # def testTagsData(self):
    #     """Testing tags data format is correct"""
    #     result = self.client.get("/user_articles/1", follow_redirects=True)
    #     self.assertIn("Recent", result.data)

if __name__ == "__main__":
    unittest.main()

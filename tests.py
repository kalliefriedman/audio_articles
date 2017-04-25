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

    def testRegister(self):
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)

    def testLogin(self):
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)

    def testCreateArticle(self):
        result = self.client.get('/create-article')
        self.assertEqual(result.status_code, 302)

    def testUserArticles(self):
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()
        result = self.client.get('/user-articles/1')
        self.assertEqual(result.status_code, 302)

    def testArticleCloseup(self):
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()
        result = self.client.get('/article-closeup/1')
        self.assertEqual(result.status_code, 302)

    def testArticleEdit(self):
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()
        result = self.client.get('/article-edit/1')
        self.assertEqual(result.status_code, 302)

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

    def testRegister(self):
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 302)

    def testLogin(self):
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 302)

    def testCreateArticle(self):
        result = self.client.get('/create-article', query_string={'user_id_from_form': "1"})
        self.assertEqual(result.status_code, 200)

    def testUserArticles(self):
        result = self.client.get('/user-articles/1')
        self.assertEqual(result.status_code, 200)

    def testArticleCloseup(self):
        result = self.client.get('/article-closeup/1')
        self.assertEqual(result.status_code, 200)

    def testArticleEdit(self):
        result = self.client.get('/article-edit/1')
        self.assertEqual(result.status_code, 200)

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

    def testTagAddProcess(self):
        result = self.client.post('/tag-add-process.json', data={"tag_value": "sample tag", "article_id": "1", "user_id_value": "1"})
        self.assertEqual(result.status_code, 200)

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


class TestDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """What needs to be done prior to each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        example_data_users()
        example_data_articles()
        example_data_tags()
        example_data_taggings()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[''] = True
        db.create_all()

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        db.drop_all()


    # def testUsersData(self):
    #     """Testing user data format is correct"""

    # def testArticlesData(self):
    #     """Testing article data format is correct"""

    # def testTagsData(self):
    #     """Testing tags data format is correct"""

    # def testTaggingsData(self):
    #     """Testing taggings data format is correct"""

    # def testBackrefs(self):
    #     """Test that backrefs work correctly as expected"""

    #     result = self.client.get("/games", data={'session["RSVP"]': True})
    #     self.assertIn("Clue", result.data)


if __name__ == "__main__":
    unittest.main()

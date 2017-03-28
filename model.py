"""Models and database functions for Audio Articles project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """User of Audio Articles app."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    password_salt = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=True)

    ds2 = db.relationship("Tag",
                          primaryjoin='User.user_id == Article.user_id',
                          secondary='join(Article, Tagging, Article.article_id == Taggings.article_id)',
                          secondaryjoin='Tagging.tagging_id == Tag.tagging_id',
                          viewonly=True,
                          )

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<User user_id=%s username=%s f_name=%s l_name=%s email=%s" +
                " phone=%s>>" % (self.user_id, self.username, self.f_name,
                                 self.l_name, self.email, self.phone))


class Article(db.Model):
    """Articles within Audio Articles app."""

    __tablename__ = "articles"

    article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    article_title = db.Column(db.String(100), nullable=False)
    article_description = db.Column(db.String(200), nullable=True)
    article_text = db.Column(db.Text, nullable=False)
    listening_progress = db.Column(db.Time, nullable=False)
    read_status = db.Column(db.Boolean, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)
    url_source = db.Column(db.String(150), nullable=True)
    last_listened = db.Column(db.DateTime, nullable=True)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("articles"))

    # Define relationship to tag
    tags = db.relationship("Tag",
                           secondary="taggings",
                           backref=db.backref("article"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Article article_id=%s user_id=%s article_title=%s" +
                " date_added=%s>" % (self.article_id, self.user_id,
                                     self.article_title, self.date_added))


class Tag(db.Model):
    """Tags in Audio Articles app."""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tag_value = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Tag tag_id=%s tag_value=%s>" % (self.tag_id, self.tag_value)


class Tagging(db.Model):
    """Taggings in Audio Articles app."""

    __tablename__ = "taggings"

    tagging_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.article_id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Tagging taggings_id=%s article_id=%s" +
                " tag_id=%s>" % (self.taggings_id,
                                 self.article_id, self.tag_id))


##############################################################################
# Helper functions

def connect_to_db(app, db_uri="postgresql:///audioarticles"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def example_data():

    # creating and adding sample users
    kallie = User(username='kfriedman', f_name='Kallie', l_name='Friedman',
                  password='password', password_salt='salt',
                  email='kallie@yahoo.com')
    db.session.add(kallie)

    natalie = User(username='nfriedman', f_name='Natalie', l_name='Friedman',
                   password='password', password_salt='salt',
                   email='natalie@hotmail.com')
    db.session.add(natalie)

    randy = User(username='rfriedman', f_name='Randy', l_name='Friedman',
                 password='password', password_salt='salt',
                 email='randy@yahoo.com')
    db.session.add(randy)

    # creating and adding sample articles
    fake_article = Article(user_id='rfriedman', article_title='Randy',
                 article_text='password', listening_progress='salt', read_status='', date_added=''
                 url_source='randy@yahoo.com')
    db.session.add(fake_article)

    fake_article = Article(user_id='rfriedman', article_title='Randy',
                 article_text='password', listening_progress='salt', read_status='', date_added=''
                 url_source='randy@yahoo.com')
    db.session.add(fake_article)

    fake_article = Article(user_id='rfriedman', article_title='Randy',
                 article_text='password', listening_progress='salt', read_status='', date_added=''
                 url_source='randy@yahoo.com')
    db.session.add(fake_article)

    fake_article = Article(user_id='rfriedman', article_title='Randy',
                 article_text='password', listening_progress='salt', read_status='', date_added=''
                 url_source='randy@yahoo.com')
    db.session.add(fake_article)

    fake_article = Article(user_id='rfriedman', article_title='Randy',
                 article_text='password', listening_progress='salt', read_status='', date_added=''
                 url_source='randy@yahoo.com')
    db.session.add(fake_article)

    fake_article = Article(user_id='rfriedman', article_title='Randy',
                 article_text='password', listening_progress='salt', read_status='', date_added=''
                 url_source='randy@yahoo.com')
    db.session.add(fake_article)

    fake_article = Article(user_id='rfriedman', article_title='Randy',
                 article_text='password', listening_progress='salt', read_status='', date_added=''
                 url_source='randy@yahoo.com')
    db.session.add(fake_article)

    fake_article = Article(user_id='rfriedman', article_title='Randy',
                 article_text='password', listening_progress='salt', read_status='', date_added=''
                 url_source='randy@yahoo.com')
    db.session.add(fake_article)

    fake_article = Article(user_id='rfriedman', article_title='Randy',
                 article_text='password', listening_progress='salt', read_status='', date_added=''
                 url_source='randy@yahoo.com')
    db.session.add(fake_article)

    fake_article = Article(user_id='rfriedman', article_title='Randy',
                 article_text='password', listening_progress='salt', read_status='', date_added=''
                 url_source='randy@yahoo.com')
    db.session.add(fake_article)

    # creating and adding sample tags



    # creating and adding sample taggings

   

    #commiting database changes
    db.session.commit()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

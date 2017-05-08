"""Models and database functions for Audio Articles project."""



from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

    tags = db.relationship("Tag",
                           primaryjoin='User.user_id == Article.user_id',
                           secondary='join(Article, Tagging, Article.article_id == Tagging.article_id)',
                           secondaryjoin='Tagging.tag_id == Tag.tag_id',
                           viewonly=True,
                           backref=db.backref("users"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<User user_id=%s username=%s f_name=%s l_name=%s email=%s phone=%s>>" % (self.user_id, self.username, self.f_name,
                self.l_name, self.email, self.phone))

    @classmethod
    def get_user_object_by_email(cls, input_email):
        user_by_email = cls.query.filter_by(email=input_email).first()
        return user_by_email

    @classmethod
    def get_user_object_by_username(cls, input_username):
        user_by_username = cls.query.filter_by(username=input_username).first()
        return user_by_username

    @classmethod
    def create_new_user(cls, username, f_name, l_name, password, email,
                        phone, password_salt):
        new_user = cls(username=username, f_name=f_name, l_name=l_name, password=password, email=email,
                       phone=phone, password_salt=password_salt)
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def get_user_object_by_user_id(cls, user_id):
        user_object = cls.query.filter_by(user_id=user_id).first()
        return user_object


class Article(db.Model):
    """Articles within Audio Articles app."""

    __tablename__ = "articles"

    article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    article_title = db.Column(db.String(100), nullable=False)
    article_description = db.Column(db.String(200), nullable=True)
    article_text = db.Column(db.Text, nullable=False)
    position = db.Column(db.Integer, default=0, nullable=False)
    read_status = db.Column(db.Boolean, default=False, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now, nullable=False)
    url_source = db.Column(db.String(150), nullable=True)
    last_listened = db.Column(db.DateTime, nullable=True)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("articles"))

    # Define relationship to tag
    tags = db.relationship("Tag",
                           secondary="taggings",
                           backref=db.backref("articles"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Article article_id=%s user_id=%s article_title=%s date_added=%s>" % (self.article_id, self.user_id,
                self.article_title, self.date_added))

    @classmethod
    def get_article_by_article_text(cls, article_text):
        article_object = cls.query.filter_by(article_text=article_text).first()
        return article_object

    @classmethod
    def get_article_by_article_id(cls, article_id):
        article_object = cls.query.filter_by(article_id=article_id).first()
        return article_object

    @classmethod
    def create_new_article(cls, article_title, user_id, article_description,
                           article_text, url_source):
        new_article = cls(article_title=article_title, user_id=user_id,
                          article_description=article_description,
                          article_text=article_text, url_source=url_source)
        db.session.add(new_article)
        db.session.commit()

    @classmethod
    def get_articles_by_user_id(cls, user_id):
        article_objects = cls.query.filter_by(user_id=user_id).all()
        return article_objects

    @classmethod
    def delete_article_with_article_id(cls, article_id):
        article_object = cls.query.filter_by(article_id=article_id).first()
        db.session.delete(article_object)
        db.session.commit()


class Tag(db.Model):
    """Tags in Audio Articles app."""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tag_value = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "%s" % (self.tag_value)

    def articles_with_tag(self, user_id):
        return db.session.query(Article).join(Tagging).filter(Tagging.tag_id == self.tag_id, Article.user_id == user_id).all()

    @classmethod
    def get_tag_by_tag_value(cls, tag_value):
        tag_object = cls.query.filter_by(tag_value=tag_value).first()
        return tag_object

    @classmethod
    def create_new_tag(cls, tag_value):
        new_tag = cls(tag_value=tag_value)
        db.session.add(new_tag)
        db.session.commit()


class Tagging(db.Model):
    """Taggings in Audio Articles app."""

    __tablename__ = "taggings"

    tagging_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.article_id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Tagging taggings_id=%s article_id=%s tag_id=%s>" % (self.tagging_id,
                self.article_id, self.tag_id))

    @classmethod
    def create_new_tagging(cls, article_id, tag_id):
            new_tagging = cls(article_id=article_id, tag_id=tag_id)
            db.session.add(new_tagging)
            db.session.commit()

    @classmethod
    def delete_taggings_with_article_id(cls, article_id):
        taggings_objects = cls.query.filter_by(article_id=article_id).all()
        for tagging in taggings_objects:
            db.session.delete(tagging)
            db.session.commit()

    @classmethod
    def delete_tagging_object(cls, tag_id, article_id):
        tagging_object = cls.query.filter(Tagging.tag_id == tag_id,
                                          Tagging.article_id == article_id).first()
        db.session.delete(tagging_object)
        db.session.commit()

##############################################################################
# Helper functions


def connect_to_db(app, db_uri="postgresql:///audioarticles"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def example_data_users():
    """creating and adding sample users"""
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

    db.session.commit()


def example_data_articles():
    """creating and adding sample articles"""

    myers_briggs = Article(user_id=1, article_title='Myers Briggs History',
                           article_text="""Katharine Cook Briggs began her research into
                           personality in 1917.""",
                           read_status=False,
                           date_added=datetime.strptime('2013-10-19', '%Y-%m-%d'),
                           url_source='wikipedia.com')
    db.session.add(myers_briggs)

    how_to = Article(user_id=1, article_title='How to make a great first impression',
                     article_text="""The initial impression you make on others is, if
                     not indelible, certainly a huge determinant in how people
                     will feel about you for quite some time. This judgment is only
                     magnified at job interviews -- an activity designed to make
                     sure you fit within an organization both personally and
                     professionally. In this Monster Special Feature, we'll cover
                     how you can make the best possible impression at the interview.
                     You'll learn how to prepare for the big day, send out the
                     right nonverbal cues, relate to the interviewer and develop
                     self-awareness of your interview image.""",
                     read_status=False,
                     date_added=datetime.strptime('2013-10-19', '%Y-%m-%d'),
                     url_source='yahoo.com')
    db.session.add(how_to)

    amazon_polly = Article(user_id=1, article_title='Amazon Polly API',
                           article_text="""Access to Amazon Polly requires credentials.
                           Those credentials must have permissions to access AWS resources,
                           such as an Amazon Polly lexicon or an Amazon Elastic Compute
                           Cloud (Amazon EC2) instance. The following sections provide
                           details on how you can use AWS Identity and Access Management
                           (IAM) and Amazon Polly to help secure access to your resources.""",
                           read_status=False,
                           date_added=datetime.strptime('2015-10-19', '%Y-%m-%d'),
                           url_source='amazon.com')
    db.session.add(amazon_polly)

    hurricane = Article(user_id=1, article_title='How hurricanes cause damage',
                        article_text="""Hurricanes are the most violent storms on Earth.
                        They form near the equator over warm ocean waters. Actually,
                        the term hurricane is used only for the large storms that form
                        over the Atlantic Ocean or eastern Pacific Ocean.""",
                        read_status=False,
                        date_added=datetime.strptime('2016-10-19', '%Y-%m-%d'),
                        url_source='weather.com')
    db.session.add(hurricane)

    peace = Article(user_id=1, article_title='How we could acheive peace',
                    article_text="""A peace treaty is an agreement between two or
                    more hostile parties, usually countries or governments, which
                    formally ends a state of war between the parties. It is
                    different from an armistice, which is an agreement to stop
                    hostilities, or a surrender, in which an army agrees to give
                    up arms, or a ceasefire or truce in which the parties may agree
                    to temporarily or permanently stop fighting.""",
                    read_status=True,
                    date_added=datetime.strptime('2017-03-19', '%Y-%m-%d'),
                    url_source='wikipedia')
    db.session.add(peace)

    engagement = Article(user_id=2, article_title='Heirarchy of Engagement',
                         article_text="""As companies move up the hierarchy, their
                         products become better, harder to leave, and ultimately create
                         virtuous loops that make the product self-perpetuating.
                         Companies that scale the hierarchy are incredibly well
                         positioned to demonstrate growth and retention that investors
                         are looking to see.""",
                         read_status=False,
                         date_added=datetime.strptime('2017-02-19', '%Y-%m-%d'),
                         url_source='medium.com')
    db.session.add(engagement)

    science = Article(user_id=2, article_title='The New Science of Exercise',
                      article_text="""Ever since high school, Dr. Mark Tarnopolsky has
                      blurred the line between jock and nerd. After working out every
                      morning and doing 200 push-ups, he runs three miles to his lab
                      at McMaster University in Ontario. When he was younger,
                      Tarnopolsky dreamed of becoming a gym teacher. But now, in his
                      backup career as a genetic metabolic neurologist, he's
                      determined to prove that exercise can be used as medicine for
                      even the sickest patients.""",
                      read_status=False,
                      date_added=datetime.strptime('2017-02-19', '%Y-%m-%d'),
                      url_source='time.com')
    db.session.add(science)

    labor_economy = Article(user_id=2, article_title='Matching Talent in The Digital Age',
                            article_text="""Online talent platforms can ease a number of
                            labor-market dysfunctions by more effectively connecting
                            individuals with work opportunities. Such platforms include
                            websites, like Monster.com and LinkedIn, that aggregate
                            workforce, we believe they can generate significant benefits
                            for economies and for individuals (exhibit).""",
                            read_status=True,
                            date_added=datetime.strptime('2016-06-23', '%Y-%m-%d'),
                            url_source='mckinsey.com')
    db.session.add(labor_economy)

    db.session.commit()


def example_data_tags():
    """creating and adding sample tags"""
    tag1 = Tag(tag_value='Recent')
    db.session.add(tag1)

    tag2 = Tag(tag_value='Favorite')
    db.session.add(tag2)

    tag3 = Tag(tag_value='Psychology')
    db.session.add(tag3)

    tag4 = Tag(tag_value='News')
    db.session.add(tag4)

    db.session.commit()


def example_data_taggings():
    """creating and adding sample taggings"""

    tagging1 = Tagging(article_id=1, tag_id=1)
    db.session.add(tagging1)

    tagging2 = Tagging(article_id=1, tag_id=1)
    db.session.add(tagging2)

    tagging3 = Tagging(article_id=8, tag_id=1)
    db.session.add(tagging3)

    tagging4 = Tagging(article_id=7, tag_id=1)
    db.session.add(tagging4)

    tagging5 = Tagging(article_id=6, tag_id=2)
    db.session.add(tagging5)

    tagging6 = Tagging(article_id=5, tag_id=2)
    db.session.add(tagging6)

    tagging7 = Tagging(article_id=4, tag_id=2)
    db.session.add(tagging7)

    tagging8 = Tagging(article_id=3, tag_id=3)
    db.session.add(tagging8)

    tagging9 = Tagging(article_id=3, tag_id=3)
    db.session.add(tagging9)

    tagging10 = Tagging(article_id=8, tag_id=4)
    db.session.add(tagging10)

    db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."

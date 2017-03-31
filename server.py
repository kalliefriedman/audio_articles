"""Routes."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Article, Tag, Tagging, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. That is bad. This will fix it.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Renders homepage if user isn't logged in. Otherwise redirects user to user-articles."""
    user_id_value = session.get("user_id")
    if user_id_value:
        return redirect("user-articles/" + str(user_id_value))
    else:
        return render_template("homepage.html")


@app.route("/register", methods=["GET"])
def register_form():
    """Renders registration form"""

    return render_template("register_form.html")


@app.route("/register-process", methods=["POST"])
def register_process():
    """Takes in four inputs via POST request and returns redirect to hompage.
    Adds new user to the database if they don't exist."""

    username = request.form.get("username")
    f_name = request.form.get("f_name")
    l_name = request.form.get("l_name")
    password = request.form.get("password")
    email = request.form.get("email")
    phone = request.form.get("phone")

    if (User.query.filter_by(email=email).all()) == []:
        new_user = User(username=username, f_name=f_name, l_name=l_name, password=password, email=email,
                        phone=phone, password_salt="")

        db.session.add(new_user)
        db.session.commit()

        user_object = User.query.filter_by(email=email).first()
        user_id = user_object.user_id
        session["user_id"] = user_id

    else:
        flash("This user already exists. Please log in.")
        return redirect("/login")

    return redirect("user-articles/" + str(user_id))


@app.route("/login", methods=["GET"])
def login_form():
    """Renders login template."""

    return render_template("login_form.html")



#what happens if i use the URL to switch between users? Which account does the article get added to? SHouldn't be able to make changes
@app.route("/login-process", methods=["POST"])
def login_process():
    """Takes in email or username, and password via post request and returns a redirect to
    either homepage or login page"""

    username_or_email = request.form.get("username_or_email")
    password = request.form.get("password")

    if User.query.filter_by(email=username_or_email).all() != []:
        user_object = User.query.filter_by(email=username_or_email).first()
    else:
        user_object = User.query.filter_by(username=username_or_email).first()

    # If user exists and password is correct, redirect to user_articles page
    if user_object and (user_object.password == password):
        session["user_id"] = user_object.user_id
        flash('You were successfully logged in.')
        return redirect("/user-articles/<userid>")
    # If either email or password incorrect, show message to user.
    else:
        flash("This combination of username and password doesn't exist")
        return redirect("/login")


@app.route("/logout", methods=["POST"])
def logout_process():
    """Takes in a post request to logout and returns redirect to homepage."""
    del session["user_id"]
    flash('You were successfully logged out')
    return redirect("/")


@app.route("/create-article")
def display_create_article():
    """Renders create article form"""
    return render_template("article_add.html")


@app.route("/user-articles/<user_id>")
def display_user_articles(user_id):
    """Takes in URL input for user_id and renders that user articles profile."""
    user_object = User.query.filter_by(user_id=user_id).one()
    return render_template("user_articles.html", user_object=user_object)


@app.route("/article-add-process", methods=["POST"])
def article_add_process():
    """Takes in four inputs via POST request and adds article to database.
    Redirects to article closeup."""
#make sure only the logged in user can add new article
    article_title = request.form.get("article_title")
    article_description = request.form.get("article_description")
    article_text = request.form.get("article_text")
    url_source = request.form.get("url_source")
    user_id_value = session.get("user_id")
# in future could verify article by same title doesn't exist

    new_article = Article(article_title=article_title, user_id=user_id_value,
                          article_description=article_description,
                          article_text=article_text, url_source=url_source)

    db.session.add(new_article)
    db.session.commit()

    article_object = Article.query.filter_by(article_text=article_text).first()
    article_id = article_object.article_id

    return redirect("article-closeup/" + str(article_id))


@app.route("/article-closeup/<article_id>")
def article_closeup(article_id):
    """Takes in an article ID and displays that article for playback and edit purposes"""

    article_object = Article.query.filter_by(article_id=article_id).one()
    return render_template("article_closeup.html", article_object=article_object)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

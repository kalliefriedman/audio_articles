"""Routes."""
from os import environ
from jinja2 import StrictUndefined

from flask import (Flask, Response, render_template, redirect, request, flash,
                   session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Article, Tag, Tagging, connect_to_db, db

from boto3 import Session as BotoSession
from datetime import datetime


#creating flask app
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. That is bad. This will fix it.
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=["GET"])
def index():
    """Renders homepage if user isn't logged in. Otherwise redirects user to user-articles."""
    # gets user id from session
    user_id_value = session.get("user_id")
    if user_id_value:
        return redirect("user-articles/" + str(user_id_value))
    else:
        return render_template("homepage.html")


@app.route("/register", methods=["GET"])
def register_form():
    """Renders registration form"""
    user_id_value = session.get("user_id")
    if user_id_value:
        return redirect("user-articles/" + str(user_id_value))
    else:
        return render_template("register_form.html")


@app.route("/register-process", methods=["POST"])
def register_process():
    """Takes in four inputs via POST request and returns redirect to hompage.
    Adds new user to the database if they don't exist."""
    user_id_value = session.get("user_id")
    username = request.form.get("username")
    f_name = request.form.get("f_name")
    l_name = request.form.get("l_name")
    password = request.form.get("password")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password_salt = ""

    if user_id_value:
        return redirect("user-articles/" + str(user_id_value))
    else:
        user_object_by_email = User.get_user_object_by_email(email)
        if user_object_by_email is None:
            User.create_new_user(username, f_name, l_name, password, email,
                                 phone, password_salt)

            user_object_by_email = User.get_user_object_by_email(email)
            user_id = user_object_by_email.user_id
            session["user_id"] = user_id

        else:
            flash("This user already exists. Please log in.")
            return redirect("/login")

        return redirect("user-articles/" + str(user_id))


@app.route("/login", methods=["GET"])
def login_form():
    """Renders login template."""
    user_id_value = session.get("user_id")
    if user_id_value:
        return redirect("user-articles/" + str(user_id_value))
    else:
        return render_template("login_form.html")


@app.route("/login-process", methods=["POST"])
def login_process():
    """Takes in email or username, and password via post request and returns a redirect to
    either homepage or login page"""
    user_id_value = session.get("user_id")
    username_or_email = request.form.get("username_or_email")
    password = request.form.get("password")

    if user_id_value:
        return redirect("user-articles/" + str(user_id_value))
    else:
        user_object = User.get_user_object_by_email(username_or_email)
        if user_object is None:
            user_object = User.get_user_object_by_username(username_or_email)

        # If user exists and password is correct, redirect to user_articles page
        if user_object and (user_object.password == password):
            session["user_id"] = user_object.user_id
            flash('You were successfully logged in.')
            return redirect("/user-articles/" + str(user_object.user_id))
        # If either email or password incorrect, show message to user.
        else:
            flash("This combination of username and password doesn't exist")
            return redirect("/login")


@app.route("/logout", methods=["POST"])
def logout_process():
    """Takes in a post request to logout and returns redirect to homepage."""
    user_id_value = session.get("user_id")
    if user_id_value:
        del session["user_id"]
        flash('You were successfully logged out')
        return redirect("/login")


@app.route("/create-article", methods=["GET"])
def display_create_article():
    """Renders create article form"""
    user_id_value = session.get("user_id")
    user_id_from_form = request.args.get("user_id_from_form")
    if user_id_value:
        if int(user_id_value) == int(user_id_from_form):
            return render_template("article_add.html", user_id=user_id_from_form)
        else:
            return redirect("user-articles/" + str(user_id_from_form))
    else:
        return redirect("/login")


@app.route("/user-articles/<int:user_id>")
def display_user_articles(user_id):
    """Takes in URL input for user_id and renders that user articles profile."""
    user_id_value = session.get("user_id")
    if user_id != user_id_value:
        return redirect("/login")
    else:
        user_object = User.get_user_object_by_user_id(user_id)
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
    # user_id_from_form = request.form.get("user_id")
    user_id_value = session.get("user_id")
# in future could verify article by same title doesn't exist
    if user_id_value:
        # if int(user_id_value) == int(user_id_from_form):
        Article.create_new_article(article_title, user_id_value,
                                   article_description,
                                   article_text, url_source)
        article_object = Article.get_article_by_article_text(article_text)
        article_id = article_object.article_id
        return redirect("article-closeup/" + str(article_id))
    else:
        return redirect("/login")


@app.route("/tag-add-process.json", methods=["POST"])
def tag_add_process():
    """Takes in two params from form via POST request and adds tag to database."""
#make sure only the logged in user can add new article
    tag_value = request.form.get("tag_value")
    article_id = request.form.get("article_id")
    user_id_value = session.get("user_id")
# in future could verify article by same title doesn't exist
    if user_id_value:
        tag_object = Tag.get_tag_by_tag_value(tag_value)
        if tag_object:
            tag_id = tag_object.tag_id
        else:
            Tag.create_new_tag(tag_value)
            tag_object = Tag.get_tag_by_tag_value(tag_value)
            tag_id = tag_object.tag_id

        Tagging.create_new_tagging(article_id, tag_id)
        new_tag_attributes = {"tag_value": tag_value, "tag_id": tag_id, "article_id": article_id}
        return jsonify(new_tag_attributes)
    else:
        return redirect("/login")


@app.route("/article-closeup/<article_id>")
def article_closeup(article_id):
    """Takes in an article ID and displays that article for playback and edit purposes"""
    user_id_value = session.get("user_id")
    article_id = int(article_id)
    article_object = Article.get_article_by_article_id(article_id)
    if user_id_value:
        if article_object.user_id == int(user_id_value):
            #using credentials for adminuser
            boto_session = BotoSession(aws_access_key_id=environ['ACCESS_KEY'],
                aws_secret_access_key=environ['SECRET_KEY'],
                region_name=environ['AWS_DEFAULT_REGION'],
                profile_name=environ['AWS_USERNAME'])
            polly = boto_session.client("polly")
            response = polly.describe_voices()
            all_voices = response.get('Voices')
            return render_template("article_closeup.html",
                                   article_object=article_object,
                                   all_voices=all_voices)
        else:
            return redirect("user-articles/" + str(user_id_value))
    else:
        return redirect("/login")


@app.route("/article-edit/<article_id>")
def article_edit(article_id):
    """Takes in an article ID and displays that article for playback and edit purposes"""
    user_id_value = session.get("user_id")
    article_object = Article.get_article_by_article_id(article_id)
    if user_id_value:
        if int(user_id_value) == article_object.user_id:
            return render_template("article_edit.html", article_object=article_object)
    else:
        return redirect("/login")


@app.route("/filter-articles/<tag_value>")
def filter_articles(tag_value):
    """Takes in a tag value via URL and returns user articles with that tag value"""
    user_id_value = session.get("user_id")
    user_tagged_articles_values = {}

    if tag_value == "All Articles":
        user_tagged_articles = Article.get_articles_by_user_id(user_id_value)
        for article in user_tagged_articles:
            user_tagged_articles_values[article.article_id] = article.article_title
    else:
        tag_object = Tag.get_tag_by_tag_value(tag_value)
        user_tagged_articles = tag_object.articles_with_tag(user_id_value)
        for article in user_tagged_articles:
            user_tagged_articles_values[article.article_id] = article.article_title

    return jsonify(user_tagged_articles_values)


@app.route("/delete-article/<article_id>", methods=['POST'])
def delete_article(article_id):
    """Takes in an article id via URL and deletes article with that article id"""
    user_id = session.get("user_id")
    Article.get_article_by_article_id(article_id)
    Tagging.delete_taggings_with_article_id(article_id)
    return redirect("/user-articles/" + str(user_id))


@app.route("/delete-tag", methods=['POST'])
def delete_tag():
    """Takes in form values via post request in URL URL and deletes tag from database"""
    tag_id = request.form.get("tag_id")
    article_id = request.form.get("article_id")
    Tagging.delete_tagging_object(tag_id, article_id)
    tag_dictionary = {"tag_id": tag_id}
    return jsonify(tag_dictionary)


@app.route("/read", methods=["GET"])
def read_text():
    """Takes in nothing, and returns an audio stream in chunks"""
    user_id_value = session.get("user_id")
    if user_id_value:
        # finds credentials associated with adminuser profile
        boto_session = BotoSession(aws_access_key_id=environ['ACCESS_KEY'],
                                   aws_secret_access_key=environ['SECRET_KEY'],
                                   region_name=environ['AWS_DEFAULT_REGION'],
                                   profile_name=environ['AWS_USERNAME'])
        polly = boto_session.client("polly")

        text = request.args.get("text")
        voice_id = request.args.get("voice")
        article_id = request.args.get("article_id")
        article_object = Article.get_article_by_article_id(int(article_id))
        if int(user_id_value) == article_object.user_id:
            response = polly.synthesize_speech(Text=text,
                                               VoiceId=voice_id,
                                               OutputFormat='mp3')

            audio_stream = response.get("AudioStream")

            if "user_id" in session:
                session_user_id = session["user_id"]
                if article_object.user_id == session_user_id:
                    article_object.read_status = True
                    article_object.last_listened = datetime.now()
                    db.session.commit()

            def generate():
                data = audio_stream.read(1024)
                while data:
                    yield data
                    data = audio_stream.read(1024)

            return Response(generate(), mimetype='audio/mpeg')
        else:
            return redirect("user-articles/" + str(user_id_value))
    else:
        return redirect("/login")
    # return Response(stream_template('user_articles.html', mimetype='audio/mpeg'))


@app.route("/user-profile")
def user_profile_react():
    """Takes in nothing and returns template for user profile"""
    user_id_value = session.get("user_id")
    if user_id_value:
        return render_template("user_profile_react.html", user_id=user_id_value)
    else:
        return redirect("/login")


@app.route("/user_info_profile.json", methods=["GET"])
def return_profile_info():
    """passes in userID and returns user info in json"""
    user_id_value = request.args.get('user_id')
    # user_id_value = session.get("user_id")
    print session
    print user_id_value
    user_object = User.get_user_object_by_user_id(user_id_value)
    user_info = {"user_id": user_object.user_id,
                 "username": user_object.username,
                 "f_name": user_object.f_name,
                 "l_name": user_object.l_name,
                 "password": user_object.password,
                 "email": user_object.email,
                 "phone": user_object.phone}
    return jsonify(user_info)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=int(environ.get("PORT", 5000)), host='0.0.0.0')
    # from gevent.wsgi import WSGIServer
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()

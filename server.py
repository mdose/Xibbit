"""Masterpiece IMDB."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (Art, Artist, User, ArtType, Collection, ArtMovement,
                   SubjectMatter, ArtistArt, UserArt, UserArtist,
                   UserCollection, connect_to_db, db)


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "IDKAnythingreally"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    # print session
    return render_template("homepage.html")


@app.route('/register', methods=["GET"])
def register_form():
    """Getting User Info from form"""

    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def process_registration_form():
    """Storing User Info"""

    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")

    if User.query.filter(User.email == email).first():
        flash("You are already registered, please log in.")
    elif User.query.filter(User.username == username).first():
        # This would work better as a popup alert on the log-in page without redirecting
        flash("Sorry. That username is already taken.")
    else:
        new_user = User(email=email, password=password, username=username)
        db.session.add(new_user)
        db.session.commit()
        session['current_user'] = new_user.user_id
        flash('You were successfully registered.')

    return redirect('/')


@app.route("/login", methods=["GET"])
def login_form():
    """Display login form. Weeeeee."""

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def process_login_form():

    email = request.form['email']
    password = request.form['password']
    user = User.query.filter(User.email == email).first()

    # print user.email, user.password

    if user and user.email == email and user.password == password:
        print session
        session['current_user'] = user.user_id
        print session
        flash("Logged in as %s" % user.user_id)
        print session
        return redirect("/")
    else:
        flash("Incorrect user or password.")
        return redirect("/login")


@app.route("/logout")
def logout():
    """Logout"""

    del(session['current_user'])

    return render_template("logout.html")


################################################################################

if __name__ == "__main__":
    # debug=True here, since it has to be True at when the DebugToolbarExtension is invoked
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

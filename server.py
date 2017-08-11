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


# Figure out how to combine registrartion and login forms onto the same page/popup
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


# Maybe 2.0: Improve form validations wtih regular expressions
    if User.query.filter(User.email == email).first():
        flash("You are already registered, please log in.")
        return redirect("/login")
    elif User.query.filter(User.username == username).first():
        # This would work better as a popup alert on the log-in page without redirecting
        flash("Sorry, that username is already taken. Please chose a different username.")
        return redirect("/register")
    else:
        new_user = User(email=email, password=password, username=username)
        db.session.add(new_user)
        db.session.commit()
        session['current_user'] = new_user.user_id
        flash('You were successfully registered, please login.')
        return redirect("/login")

    # return redirect('/')


@app.route("/login", methods=["GET"])
def login_form():
    """Displays login form."""

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def process_login_form():
    """Handles login form data and redirects to correct route"""

# Maybe 2.0: Improve form validations wtih regular expressions
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter(User.email == email).first()
    #user_id = User.query.filter_by(user_id=user_id).first()

    # print user.email, user.password

    if user and user.email == email and user.password == password:
        session['current_user'] = user.user_id
        flash("Logged in as %s" % user.username)
        return render_template("profile.html", user=user)
        # return redirect("/users/<user_id>")
        # getting data error invalid input syntax for integer: when I try to
        # redirect to this route, but works with rendering template. Why?
    else:
        flash("Incorrect user or password.")
        return redirect("/login")


# Figure out how to handle edge case when someone clicks this button and there is
# no cookie session.
# intial ideas include toggling the button with jQuery and/or redirecting to homepage
# with flash message stating that user is not logged in.
@app.route("/logout")
def logout():
    """Logout"""

    # if 'current_user' == None:
    #     flash("You can't logout because you aren't logged in. Please login")
    #     return redirect("/login")
    # else:
    flash("Goodbye")
    del(session['current_user'])
    return render_template("logout.html")


@app.route("/users/<user_id>")
def user(user_id):
    """Generates the profile page for each user in db."""

    user = User.query.filter_by(user_id=user_id).first()
    if user == None:
        flash("User %s not found." % user_id)
        return redirect("/login")

    return render_template("profile.html",
                          user=user)

################################################################################

if __name__ == "__main__":
    # debug=True here, since it has to be True at when the DebugToolbarExtension is invoked
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

"""Masterpiece IMDB."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import (Art, Artist, User, ArtType, Collection, ArtMovement,
                   SubjectMatter, ArtistArt, UserArt, UserArtist,
                   UserCollection, connect_to_db, db)


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "IDKAnythingreally"

app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/', methods=["GET"])
def show_index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/', methods=["POST"])
def search_db():
    """Query that searches the Database"""

    # TODO: Account for so, so many edge cases.
    # TODO: Create search results tempalate instead of redirecting to one page

    search = request.form.get("search")
    artworks = Art.query.filter(Art.title == search).all()
    artists = Artist.query.filter(Artist.primary_name == search).all()
    museums = Collection.query.filter(Collection.name == search).all()

    if artworks or artists or museums:
        return render_template("results.html", search=search, artworks=artworks,
                               artists=artists, museums=museums)
    else:
        flash("I'm sorry, that term has not been added to the database. Please search again.")
        return redirect("/")


@app.route('/register', methods=["GET"])
def show_register_form():
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
        user = User.query.filter(User.email == email).first()
        session['current_user'] = new_user.user_id
        flash('You were successfully registered and logged in.')
        return redirect("/users/" + str(user.user_id))


@app.route("/login", methods=["GET"])
def show_login_form():
    """Displays login form."""

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def process_login_form():
    """Handles login form data and redirects to correct route"""

# Maybe 2.0: Improve form validations wtih regular expressions
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter(User.email == email).first()

    if user and user.email == email and user.password == password:
        # Posssible instead of "current_user" to directly get user_id and email from
        # session dict (Refactoring?). Would also have to change/reverse it on logout.
        session['current_user'] = user.user_id
        flash("Logged in as %s" % user.username)
        # return render_template("profile.html", user=user)
        return redirect("/users/" + str(user.user_id))

    else:
        flash("Incorrect user or password.")
        return redirect("/login")


@app.route("/logout")
def show_logout():
    """Logout"""

    flash("Goodbye")
    del(session['current_user'])
    return render_template("logout.html")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Generates the profile page for each user in db."""

    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        flash("User %s not found." % user_id)
        return redirect("/login")

    return render_template("profile.html", user=user)


@app.route("/toggle/art.json")
def toggle_fav_art_to_db():
    """Toggle art favorited by a user to to UserArt Table"""

    user_id = session['current_user']
    art_id = request.args.get("art_id")
    # getting art_id via js object key rather than "name" HTML element

    favorite_art = UserArt.query.filter_by(user_id=user_id, art_id=art_id).first()

    if favorite_art:
        # If favorite already exists in db for this user, remove it
        # user_list.artworks.pop(favorite)
        db.session.delete(favorite_art)
        db.session.commit()

    else:
        new_favorite_art = UserArt(user_id=user_id, art_id=art_id)
        # If favorite already exists in db for this user, add it
        # user_list.artworks.append(favorite)
        db.session.add(new_favorite_art)
        db.session.commit()

    result = "Success!"

    return result


@app.route("/toggle/artist.json")
def toggle_fav_artist_to_db():
    """Toggle artist favorited by a user to to UserArtist Table"""

    user_id = session['current_user']
    artist_id = request.args.get("artist_id")

    favorite_artist = UserArtist.query.filter_by(user_id=user_id, artist_id=artist_id).first()

    if favorite_artist:
        db.session.delete(favorite_artist)
        db.session.commit()

    else:
        new_favorite_artist = UserArtist(user_id=user_id, artist_id=artist_id)
        db.session.add(new_favorite_artist)
        db.session.commit()

    result = "Success!"

    return result


@app.route("/toggle/collection.json")
def toggle_fav_collection_to_db():
    """Toggle collection favorited by a user to to UserCollection Table"""

    user_id = session['current_user']
    collection_id = request.args.get("collection_id")

    favorite_collection = UserCollection.query.filter_by(user_id=user_id, collection_id=collection_id).first()

    if favorite_collection:
        db.session.delete(favorite_collection)
        db.session.commit()

    else:
        new_favorite_collection = UserCollection(user_id=user_id, collection_id=collection_id)
        db.session.add(new_favorite_collection)
        db.session.commit()

    result = "Success!"

    return result


@app.route('/artworks')
def show_art_list():
    """Show list of artworks in db"""

    artworks = Art.query.all()
    return render_template("art_list.html", artworks=artworks)


@app.route("/artworks/<art_id>")
def show_art(art_id):
    """Generates the display page for each artwork in db."""

    art = Art.query.filter_by(art_id=art_id).first()
    if 'current_user' in session:
        user_id = session['current_user']
        favorite = UserArt.query.filter_by(user_id=user_id, art_id=art_id).first()
        is_favorited = favorite is not None
    else:
        is_favorited = False

    return render_template("artworks.html", art=art, is_favorited=is_favorited)


@app.route('/artists')
def show_artist_list():
    """Show list of artists in db"""

    artists = Artist.query.all()
    return render_template("artist_list.html", artists=artists)


@app.route("/artists/<artist_id>")
def show_artist(artist_id):
    """Generates the display page for each artist in db."""

    artist = Artist.query.filter_by(artist_id=artist_id).first()
    if 'current_user' in session:
        user_id = session['current_user']
        favorite = UserArtist.query.filter_by(user_id=user_id, artist_id=artist_id).first()
        is_favorited = favorite is not None
    else:
        is_favorited = False

    return render_template("artists.html", artist=artist, is_favorited=is_favorited)


@app.route('/collections')
def show_collection_list():
    """Show list of collections in db"""

    collections = Collection.query.all()
    return render_template("museums_list.html", collections=collections)


@app.route("/collections/<collection_id>")
def show_collection(collection_id):
    """Generates the display page for each collection in db."""

    collection = Collection.query.filter_by(collection_id=collection_id).first()
    if 'current_user' in session:
        user_id = session['current_user']
        favorite = UserCollection.query.filter_by(user_id=user_id, collection_id=collection_id).first()
        is_favorited = favorite is not None
    else:
        is_favorited = False

    return render_template("museums.html", collection=collection, is_favorited=is_favorited)

################################################################################

if __name__ == "__main__":
    # debug=True here, since it has to be True at when the DebugToolbarExtension is invoked
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

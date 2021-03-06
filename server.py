"""Xibbit."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from passlib.hash import pbkdf2_sha256

from model import (Art, Artist, User, ArtType, Collection, ArtMovement,
                   SubjectMatter, ArtistArt, UserArt, UserArtist,
                   UserCollection, Label, LabelArt, connect_to_db, db)

# pip install geocoder
# TODO: ^ geocoder will be needed for creating the v. 3.0 admin form of adding new
# data/museums to db. Form will have user enter museum address and geocoder will
# convert that into lat and long and put into db automatically (more advanced use
# of Maps API with the python geocoder library.)
# TODO: Google Cloud Vision will need to add labels to db when admin form commits
# to db(both APIS will need to be considered)

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "IDKAnythingreally"

app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/', methods=["GET"])
def show_index():
    """Homepage."""

    return render_template("homepage.html", background_img=True)

@app.route('/about', methods=["GET"])
def show_about():
    """About the app."""

    return render_template("about.html")


@app.route('/results', methods=["GET"])
def search_db():
    """Query that searches the Database"""

    search = request.args.get("search")
    subquery = db.session.query(Label.label_id).filter(Label.label.ilike('%' + search + '%')).subquery()
    artworks = db.session.query(Art).join(SubjectMatter).join(LabelArt).join(ArtType).join(ArtMovement).filter(SubjectMatter.category.ilike('%' + search + '%') | Art.title.ilike('%' + search + '%') | LabelArt.label_id.in_(subquery) | ArtType.art_type.ilike('%' + search + '%') | ArtMovement.movement_name.ilike('%' + search + '%')).all()
    artists = Artist.query.filter(Artist.primary_name.ilike('%' + search + '%')).all()
    museums = Collection.query.filter(Collection.name.ilike('%' + search + '%') | Collection.location.ilike('%' + search + '%')).all()

    if artworks or artists or museums:
        return render_template("results.html", search=search, artworks=artworks,
                               artists=artists, museums=museums)
    else:
        flash("I'm sorry, that term has not yet been added to the database. Please try again.")
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

    hashed = pbkdf2_sha256.hash(password)
    del password

# Maybe 2.0: Improve form validations wtih regular expressions
    if User.query.filter(User.email == email).first():
        flash("You are already registered, please log in.")
        return redirect("/login")
    elif User.query.filter(User.username == username).first():
        # This would work better as a popup alert on the log-in page without redirecting
        flash("Sorry, that username is already taken. Please chose a different username.")
        return redirect("/register")
    else:
        new_user = User(email=email, password=hashed, username=username)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter(User.email == email).first()
        session['current_user'] = new_user.user_id
        flash('You were successfully registered and logged in.')
        return redirect("/profile")


@app.route("/login", methods=["GET"])
def show_login_form():
    """Displays login form."""

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def process_login_form():
    """Handles login form data and redirects to correct route"""

# Maybe 2.0: Improve form validations wtih regular expressions
    email = request.form['email']
    attempt = request.form['password']
    user = User.query.filter(User.email == email).first()

# user.password is the stored hashed pwd in the db (no passwords stored in plain text)
    if user and pbkdf2_sha256.verify(attempt, user.password):
        # Posssible instead of "current_user" to directly get user_id and email from
        # session dict (Refactoring?). Would also have to change/reverse it on logout.
        session['current_user'] = user.user_id
        flash("Logged in as %s" % user.username)
        # return render_template("profile.html", user=user)
        return redirect("/profile")

    else:
        flash("Incorrect user or password.")
        return redirect("/login")


@app.route("/logout")
def show_logout():
    """Logout"""

    flash("Goodbye")
    del(session['current_user'])
    return render_template("logout.html")


@app.route("/profile")
def show_user():
    """Generates the profile page for each user in db."""

    user_id = session['current_user']
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        flash("User %s not found." % user_id)
        return redirect("/login")

    # TODO get lat/lng from db and make markers render on map (in two colors to
    # distinguish b/t fav art and fav museums)

    return render_template("profile.html", user=user)


@app.route('/get_info')
def get_info():
    """Gets db info needed to generate map markers that shows the museum locations of a user's favorite art"""
    user_id = session['current_user']
    subquery = db.session.query(UserArt.art_id).filter(UserArt.user_id == user_id).subquery()
    fav_arts = Art.query.filter(Art.art_id.in_(subquery)).all()
    # returns a list of all art favorited by current user
    fav_art_dict = {'favorites': {}}
    # empty dictionary fav_art contains a dictionary for it's values

    for art in fav_arts:
        # loop through list of artworks in the fav_arts query list
        art_info = {'art_id': art.art_id,
                    'title': art.title,
                    'collection': art.collection.name,
                    'website': art.collection.website,
                    'location': {'lat': art.collection.lat,
                                 'lng': art.collection.lng
                                 }
                    }
        # for each artwork create an art_info variable with a dictionary as it's value
        # inside that dictionary have a string as a keyword and info from the database as the value
        # except for the key 'location', which has another dict as it's value with lat/lng as keys and nums as values
        key = "["+str(art.collection.lat)+", "+str(art.collection.lng)+"]"
        if not key in fav_art_dict['favorites']:
            fav_art_dict['favorites'][key] = []
            # make lat and long a list as a key, with an empty list as it's value

        fav_art_dict['favorites'][key].append(art_info)
        # then for each art_info box created, append that to the empty value list for the lat/long key

    return jsonify(fav_art_dict)
    # jsonify the favorites dict to send to the JS/Client


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

    return "Success!"


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
    app.debug = False
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0', port=5000)

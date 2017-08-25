"""Models and database functions for masterpieces db."""

from flask_sqlalchemy import SQLAlchemy

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Compose ORM

class Art(db.Model):
    """Art model"""

    __tablename__ = "artworks"

    art_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True,
                       nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(1000), nullable=False)
    # !!!Remember to add a constraint to db or server that insures that year or
    # year description is required to add art to the database (all are nullable)
    year = db.Column(db.Integer, nullable=True)
    year_range = db.Column(db.Integer, nullable=True)
    circa = db.Column(db.Boolean, nullable=True)
    year_description = db.Column(db.String(50), nullable=True)
    medium = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    height_cm = db.Column(db.Float, nullable=True)
    width_cm = db.Column(db.Float, nullable=True)
    collection_id = db.Column(db.Integer,
                              db.ForeignKey('collections.collection_id'),
                              nullable=False)
    art_type_id = db.Column(db.Integer,
                            db.ForeignKey('art_types.art_type_id'),
                            nullable=False)
    art_movement_id = db.Column(db.Integer,
                                db.ForeignKey('art_movements.art_movement_id'),
                                nullable=False,)
    subject_matter_id = db.Column(db.Integer,
                                  db.ForeignKey('subject_matters.subject_matter_id'),
                                  nullable=False)

    # establishes relationship thanks to the Foreign Key
    collection = db.relationship('Collection', backref='artworks')
    art_type = db.relationship('ArtType', backref='artworks')
    art_movement = db.relationship('ArtMovement', backref='artworks')
    subject_matter = db.relationship('SubjectMatter', backref='artworks')
    artists = db.relationship('Artist', secondary='artists_artworks', backref='artworks')

    def __repr__(self):
        """Info on artworks"""

        return """
        <Artwork id: {}, Title: {}, Image: {}, Date: {}{}-{} {}, Medium: {},
        Description: {}, Height {}, Witdh {}, Collection id: {}, ArtType id: {},
        ArtMovement: {}, SubjectMatter: {}>
        """.format(self.art_id, self.title, self.image_url, self.circa, self.year,
                   self.year_range, self.year_description, self.medium, self.description,
                   self.height_cm, self.width_cm, self.collection_id, self.art_type_id,
                   self.art_movement_id, self.subject_matter_id)


class Artist(db.Model):
    """Artist model"""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True,
                          nullable=False)
    # primary_name is the SURNAME of the artist, "Unknown artist", or ONLY artist name
    primary_name = db.Column(db.String(100), nullable=False)
    # secondary_name is the GIVEN name of the artist
    secondary_name = db.Column(db.String(100), nullable=True)
    birth_year = db.Column(db.Integer, nullable=True)
    death_year = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.String(10000), nullable=False)
    image_url = db.Column(db.String(1000), nullable=True)
    image_caption = db.Column(db.String(10000), nullable=True)

    def __repr__(self):
        """Info on artists"""

        return "<Artist id: {}, Name: {}, {}, Lifespan: {} - {}, Bio: {}, Image: {}, Caption: {}>".format(
            self.artist_id, self.primary_name, self.secondary_name, self.birth_year,
            self.death_year, self.bio, self.image_url, self.image_caption)


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    # For 2.0 -> image_url = db.Column(db.String(500), nullable=True)

    artworks = db.relationship('Art', secondary='users_artworks', backref='users')
    artists = db.relationship('Artist', secondary='users_artists', backref='users')
    collections = db.relationship('Collection', secondary='users_collections',
                                  backref='users')

    def __repr__(self):
        """Info on Users"""

        return "<User id: {}, Email: {},  Password: {}, Username: {}>".format(
            self.user_id, self.email, self.password, self.username)


class ArtType(db.Model):
    """Type of an artwork (ex. painting, sculpture, ceramics, etc.) Model"""

    __tablename__ = "art_types"

    art_type_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,
                            nullable=False)
    art_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Info on Art Types"""

        return "<Id: {}, Art Type: {}>".format(self.art_type_id, self.art_type)


class Collection(db.Model):
    """Where the artwork currently lives Model"""

    __tablename__ = "collections"

    collection_id = db.Column(db.Integer,
                              primary_key=True,
                              autoincrement=True,
                              nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """Info on museum or collection the artwork belongs to"""

        return "<Collection id: {}, Institution name: {}, Location: {}, Image_URL: {}, Address: {}, Lat: {}, Lng: {}>".format(
            self.collection_id, self.name, self.location, self.image_url, self.address,
            self.lat, self.lng)


class ArtMovement(db.Model):
    """Primary artistic movement the artwork is associated with Model"""

    __tablename__ = 'art_movements'

    art_movement_id = db.Column(db.Integer,
                                primary_key=True,
                                autoincrement=True,
                                nullable=False)
    movement_name = db.Column(db.String(50), nullable=False)
    # make descriptions not nullable once you add them to the seed data!!!
    description = db.Column(db.String(10000), nullable=True)

    def __repr__(self):
        """Info on the different art movements"""

        return "<Art Movement id: {}, Movement name: {}, Description: {}>".format(
            self.art_movement_id, self.movement_name, self.description)


class SubjectMatter(db.Model):
    """Primary classification of the artwork within traditional art sphere Model"""
    """Ex. Portrait, Landscape, Still Life, etc."""

    __tablename__ = "subject_matters"

    subject_matter_id = db.Column(db.Integer,
                                  primary_key=True,
                                  autoincrement=True,
                                  nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Info on the different traditional art subject matters"""

        return "<Subject Matter id: {}, Category {}>".format(
            self.subject_matter_id, self.category)


class ArtistArt(db.Model):
    """Association table for Artists and Artworks"""

    __tablename__ = "artists_artworks"

    artist_art_id = db.Column(db.Integer,
                              primary_key=True,
                              autoincrement=True,
                              nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'), nullable=False)
    art_id = db.Column(db.Integer, db.ForeignKey('artworks.art_id'), nullable=False)

    def __repr__(self):
        """Info for Artist/Art Table"""

        return "<Artist/Art id: {}, Artist id: {}, Art id: {}>".format(
            self.artist_art_id, self.artist_id, self.art_id)


class UserArt(db.Model):
    """Association table for Users and Artworks"""

    __tablename__ = "users_artworks"

    user_art_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,
                            nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    art_id = db.Column(db.Integer, db.ForeignKey('artworks.art_id'), nullable=False)
    # list_id (2.0)

    def __repr__(self):
        """Info on the User/Art Table"""

        return "<User/Art id: {}, User id: {}, Art id: {}>".format(
            self.user_art_id, self.user_id, self.art_id)


class UserArtist(db.Model):
    """Association table for Users and Artists"""

    __tablename__ = "users_artists"

    user_artist_id = db.Column(db.Integer,
                               primary_key=True,
                               autoincrement=True,
                               nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'), nullable=False)
    # list_id (2.0)

    def __repr__(self):
        """Info on the User/Artist Table"""

        return "<User/Artist id: {}, User id: {}, Artist id: {}>".format(
            self.user_artist_id, self.user_id, self.artist_id)


class UserCollection(db.Model):
    """Association table for Users and Collections/Museums"""

    __tablename__ = "users_collections"

    user_collection_id = db.Column(db.Integer,
                                   primary_key=True,
                                   autoincrement=True,
                                   nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.collection_id'),
                              nullable=False)
    # list_id (2.0)

    def __repr__(self):
        """Info on the User/Collection Table"""

        return "<User/Collection id: {}, User id: {}, Collection: {}>".format(
            self.user_collection_id, self.user_id, self.collection_id)


# class ArtworkArtMovement(db.Model):
#     """Association table for Artworks and ArtMovements"""

#     __tablename__ = "artworks_artmovements"

#     pass


# class ArtworkSubjectMatter(db.Model):
#     """Association table for Artworks and Subject Matter"""

#     pass

########### Version 2.0  ######################################################
# class Content(db.Model):
#     """Content labels for users to find what's in an artwork"""
#     """Ex. Dog, Cat, boy, girl, etc."""
#     """To be used with Google API"""

#     pass


# class ArtworkContent(db.Model):
#     """Association table for Artworks and Content"""

#     pass

##############################################################################
# Helper functions

def connect_to_db(app, database='postgres:///masterpieces'):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

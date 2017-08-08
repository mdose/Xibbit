"""Models and database functions for masterpieces db."""

from flask_sqlalchemy import SQLAlchemy

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Compose ORM

class Artwork(db.Model):
    """Art model"""

    ___tablename__ = "artworks"

    artwork_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                           nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    # Find out if there is Datetime Library for BCE and CE dates and circa
    date = db.Column(db.String(30), nullable=False)
    medium = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    # Find out if there is a measurement Library for numbers
    height = db.Column(db.String(50), nullable=True)
    width = db.Column(db.String(50), nullable=True)
    # depth = db.Column(db.String(50), nullable=True)
    collection_id = db.Column(db.Integer, nullable=False,
                              db.ForeignKey('collections.collection_id'))
    art_type_id = db.Column(db.Integer, nullable=False,
                              db.ForeignKey('art_types.art_type_id')

    # establishes relationship thanks to the Foreign Key
    collection = db.relationship('Collection', backref='artworks')
    art_type = db.relationship('ArtType', backref="art_types")

    def __repr__(self):
        """Info on artworks"""

        return "<Artwork id: {}, Title: {}, Image: {}, Date: {}, Medium: {}, Description: {}, Height {}, Witdh {}, Collection id: {}, ArtType id: {}>".format(
            self.artwork_id, self.title, self.image_url, self.date, self.medium, self.description, self.height, self.width, self.collection_id, self.art_type_id)


class Artist(db.Model):
    """Artist model"""

    ___tablename__ = "artists"

    artist_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                           nullable=False)
    # primary_name is the SURNAME of the artist, "Unknown artist", or ONLY
    # artist name (ex. Myron of Ancient Greece)
    primary_name = db.Column(db.String(100), nullable=False)
    # secondary_name is the GIVEN name of the artist
    secondary_name = db.Column(db.String(100), nullable=True)
    birth_year = db.Column(db.Integer, nullable=True)
    death_year = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        """Info on artists"""

        return "<Artist id: {}, Name: {}, {}, Lifespan: {} - {}, Bio: {}, Image: {}>".format(
            self.artist_id, self.primary_name, self.secondary_name, self.birth_year, self.death_year, self.bio, self.image_url)


class User(db.Model):
    """User info"""

    pass


class ArtType(db.Model):
    """Type of an artwork (ex. painting, sculpture, ceramics, etc.)"""

    pass


class Collection(db.Model):
    """Where the artwork currently live"""

    pass


class ArtMovement(db.Model):
    """Type of artistic movement(s) the artwork is associated with"""

    pass


class ArtworkArtMovement(db.Model):
    """Association table for Artworks and ArtMovements"""

    ___tablename__ = "artworks_artmovements"

    pass


class SubjectMatter(db.Model):
    """Classification of the artwork within traditional art sphere"""
    """Ex. Portrait, Landscape, Still Life, etc."""

    pass


class ArtworkSubjectMatter(db.Model):
    """Association table for Artworks and Subject Matter"""

    pass


class ArtistArtwork(db.Model):
    """Association table for Artists and Artworks"""

    pass


class FavoritedArtwork(db.Model):
    """Association table for Users and Artworks"""

    pass


class FavoritedArtist(db.Model):
    """Association table for Users and Artists"""

    pass


class FavoritedCollection(db.Model):
    """Association table for Users and Collections/Museums"""

    pass



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

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///masterpieces'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

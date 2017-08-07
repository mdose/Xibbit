"""Models and database functions for masterpieces db."""

from flask_sqlalchemy import SQLAlchemy

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Compose ORM

class Artwork(db.Model):
    """Art info"""

    ___tablename__ = "artworks"


class Artist(db.Model):
    """Artist info"""

    pass


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

"""Utility file to seed masterpieces database from seed_data/"""

# from sqlalchemy import func
from model import Art
from model import Artist
from model import ArtType
from model import Collection
# from model import ArtMovement
# from model import ArtistArt
# from model import UserArt
# from model import UserArtist
# from model import UserCollection

from model import connect_to_db, db
from server import app


def load_art():
    """Load artworks from u.art into database."""

    print "Art"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate art
    Art.query.delete()

    # Read u.art file and insert data
    for row in open("seed_data/u.art"):
        # NOTE: Google puts carriage return \n AND new feed combo at the end of
        # coverted tvs files (hence the janky fix).
        # Possible TO DO: refactor with built-in cvs module (using tvs for now b/c of commas)
        row = row.rstrip("\n").strip(chr(13))
        row = row.split("\t")
        art_id = row[0]
        title = row[1]
        image_url = row[2]
        circa = row[3]
        year = row[4] if row[4] else None
        year_range = row[5] if row[5] else None
        year_description = row[6]
        medium = row[7]
        description = row[8]
        height_cm = row[9]
        width_cm = row[10] if row[10] else None
        art_type_id = row[11]
        collection_id = row[12]

        art = Art(art_id=art_id, title=title, image_url=image_url, circa=circa,
                  year=year, year_range=year_range, year_description=year_description,
                  medium=medium, description=description, height_cm=height_cm,
                  width_cm=width_cm, art_type_id=art_type_id, collection_id=collection_id)


        # We need to add to the session or it won't ever be stored
        db.session.add(art)

    # Once we're done, we should commit our work
    db.session.commit()


def load_artists():
    """Load artists from u.artists into database."""

    print "Artists"

    Artist.query.delete()

    for row in open("seed_data/u.artists"):
        row = row.rstrip("\n").strip(chr(13))
        row = row.split("\t")
        artist_id = row[0]
        primary_name = row[1]
        secondary_name = row[2] if row[2] else None
        birth_year = row[3] if row[3] else None
        death_year = row[4] if row[4] else None
        bio = row[5]
        image_url = row[6] if row[6] else None

        artist = Artist(artist_id=artist_id, primary_name=primary_name,
                        secondary_name=secondary_name, birth_year=birth_year,
                        death_year=death_year, bio=bio, image_url=image_url)

        db.session.add(artist)

    db.session.commit()


def load_art_type():
    """Load artypes from u.art_types into database."""

    print "Art Types"

    ArtType.query.delete()

    for row in open("seed_data/u.art_types"):
        row = row.rstrip("\n").strip(chr(13))
        row = row.split("\t")
        art_type_id, art_type = row

        art_type = ArtType(art_type_id=art_type_id, art_type=art_type)
        db.session.add(art_type)

    db.session.commit()


def load_collection():
    """Load collections from u.collecetions into database."""

    print "Collections"

    Collection.query.delete()

    for row in open("seed_data/u.collections"):
        row = row.rstrip("\n").strip(chr(13))
        row = row.split("\t")
        collection_id, name, location = row

        collection = Collection(collection_id=collection_id, name=name, location=location)
        db.session.add(collection)

    db.session.commit()


##############################################################################
# for 3.0 add more info to db forms; the solution below is for if it's just one
# table. If more than one, Katie has a solution to make more d.r.y. with special
# func she sent via Slack!

# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_art_type()
    load_collection()
    load_art()
    load_artists()

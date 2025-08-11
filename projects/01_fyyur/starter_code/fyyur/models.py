from . import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Association table
venue_genres = db.Table('venue_genres',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genres.id'), primary_key=True)
)

artist_genres = db.Table('artist_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genres.id'), primary_key=True)
)

class Genres(db.Model):
  __tablename__ = 'Genres'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  genre = db.Column(db.String, nullable=False, unique=True)

  def __repr__(self):
    return f'<Genres {self.id} {self.genre}>'

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship('Genres', secondary=venue_genres, backref=db.backref('genres', lazy=True))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Shows', backref='venue', lazy=True)

    def __repr__(self):
      return f'<Venue {self.id} {self.name}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship('Genres', secondary=artist_genres, backref=db.backref('genres_of_artist', lazy=True))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))

class Shows(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'), nullable=False)
    artist = db.relationship('Artist', backref='shows')
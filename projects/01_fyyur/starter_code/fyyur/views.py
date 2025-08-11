
import json
import dateutil.parser
import babel
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from collections import defaultdict
from fyyur.forms import *
from fyyur.models import Venue, Artist, Genres, Shows
from . import db

main = Blueprint('main', __name__)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@main.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@main.route('/venues')
def venues():

  now = datetime.now()
  venues = Venue.query.order_by('name').all()

  city_state_map = defaultdict(list)

  for venue in venues:
    num_upcoming_shows = sum(1 for show in venue.shows if show.start_time > now)

    city_state_map[(venue.city, venue.state)].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": num_upcoming_shows
    })

  data = []
  for (city, state), venues_list in city_state_map.items():
    data.append({
        "city": city,
        "state": state,
        "venues": venues_list
    })

  return render_template('pages/venues.html', areas=data)

@main.route('/venues/search', methods=['POST'])
def search_venues():

  now = datetime.now()

  search_term = request.form['search_term']
  all_venues = Venue.query
  results = all_venues.filter(Venue.name.ilike('%' + search_term + '%')).all()

  venues = []
  for result in results:
    num_upcoming_shows = sum(1 for show in result.shows if show.start_time > now)
    venues.append({"id": result.id, "name": result.name, "num_upcoming_shows": num_upcoming_shows})
  
  response = {
    "count": len(results),
    "data": venues
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@main.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  now = datetime.now()

  venue = Venue.query.get(venue_id)

  past_shows = []
  upcoming_shows = []

  for show in venue.shows:
    artist = show.artist
    show_data = {
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": show.start_time.isoformat()
    }
    if show.start_time < now:
        past_shows.append(show_data)
    else:
        upcoming_shows.append(show_data)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": [genre.genre for genre in venue.genres], 
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@main.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@main.route('/venues/create', methods=['POST'])
def create_venue_submission():

  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():

    genre_objects = []
    for genre_name in form.genres.data:
      genre = Genres.query.filter_by(genre=genre_name).first()
      genre_objects.append(genre)

    try:
      venue = Venue(
          name=form.name.data,
          city=form.city.data,
          state=form.state.data,
          address=form.address.data,
          phone=form.phone.data,
          image_link=form.image_link.data,
          facebook_link=form.facebook_link.data,
          website_link=form.website_link.data,
          genres=genre_objects,  
          seeking_talent=form.seeking_talent.data,
          seeking_description=form.seeking_description.data 
      )
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + form.name.data + ' was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    finally:
      db.session.close()

  return render_template('pages/home.html')

@main.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  error = False
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    flash('Venue ' + venue.name + ' could not be deleted')
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + venue.name + ' was successfully deleted!')
  
  return jsonify({ 'success': True })

#  Artists
#  ----------------------------------------------------------------
@main.route('/artists')
def artists():
  data = Artist.query.order_by('name').all()
  return render_template('pages/artists.html', artists=data)

@main.route('/artists/search', methods=['POST'])
def search_artists():

  now = datetime.now()

  search_term = request.form['search_term']
  all_artists = Artist.query.order_by('name')
  results = all_artists.filter(Artist.name.ilike('%' + search_term + '%')).all()

  artists = []
  for result in results:
    num_upcoming_shows = sum(1 for show in result.shows if show.start_time > now)
    artists.append({"id": result.id, "name": result.name, "num_upcoming_shows": num_upcoming_shows})
  
  response = {
    "count": len(results),
    "data": artists
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@main.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  now = datetime.now()
  artist = Artist.query.get(artist_id)

  past_shows = []
  upcoming_shows = []

  for show in artist.shows:
    venue = show.venue
    show_data = {
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": show.start_time.isoformat()
    }
    if show.start_time < now:
        past_shows.append(show_data)
    else:
        upcoming_shows.append(show_data)

  data={
    "id": artist.id,
    "name": artist.name,
    "genres": [genre.genre for genre in artist.genres],
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@main.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  form.name.data = artist.name
  form.state.data = artist.state
  form.city.data = artist.city
  form.genres.data = [genre.genre for genre in artist.genres]
  form.phone.data = artist.phone
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website_link.data = artist.website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@main.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  artist = Artist.query.get(artist_id)

  try:
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.website_link = request.form['website_link']
    artist.seeking_venue = True if request.form['seeking_venue'] == 'y' else False
    artist.seeking_description = request.form['seeking_description']
    artist.genre_names = request.form.getlist('genres')

    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@main.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  form.name.data = venue.name
  form.state.data = venue.state
  form.city.data = venue.city
  form.address.data = venue.address
  form.genres.data = [genre.genre for genre in venue.genres]
  form.phone.data = venue.phone
  form.facebook_link.data = venue.facebook_link
  form.image_link.data = venue.image_link
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@main.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  venue = Venue.query.get(venue_id)

  try:
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website_link = request.form['website_link']
    venue.seeking_talent = True if request.form['seeking_talent'] == 'y' else False
    venue.seeking_description = request.form['seeking_description']
    venue.genre_names = request.form.getlist('genres')

    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@main.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@main.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form, meta={'csrf': False})
  if form.validate():

    genre_objects = []
    for genre_name in form.genres.data:
      genre = Genres.query.filter_by(genre=genre_name).first()
      genre_objects.append(genre)

    try:
      artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        genres=genre_objects,  
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data 
      )
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + form.name.data + ' was successfully listed!')
    except Exception as e:
      print(e)
      db.session.rollback()
      flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    finally:
      db.session.close()
  else:
    print(form.errors)

  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@main.route('/shows')
def shows():
  query = Shows.query.order_by('start_time').all()

  shows = []

  for show in query:
    data = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.isoformat()
    }
    shows.append(data)

  return render_template('pages/shows.html', shows=shows)

@main.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@main.route('/shows/create', methods=['POST'])
def create_show_submission():

  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    show = Shows(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    flash('There was an error and your show could not be listed')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@main.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

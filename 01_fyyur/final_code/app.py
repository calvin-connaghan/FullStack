#----------------------------------------------------------------------------#
# Imports - DONE
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

#CC - Import Migrate for DB connection
from flask_migrate import Migrate

#CC - Import Datetime for Now variable
from datetime import datetime

#CC - Import func for areas variable
from sqlalchemy import func

#----------------------------------------------------------------------------#
# App Config - DONE
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# [DONE] Connect to a local postgresql database
#CC - Set Migrate equal to app name and SQLAlchemy.
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models - DONE
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # [DONE] implement any missing fields, as a database migration using Flask-Migrate
    
    #CC - Added to cover missing field. Used array column to store multiple genres.
    genres = db.Column(db.ARRAY(db.String)) 
    
    #CC - Added to cover missing field.
    website = db.Column(db.String(120))
    
    #CC - Added to cover missing field. Venue not seeking artists as default.
    seeking_talent = db.Column(db.Boolean, default=False) 
    
    #CC - Added to cover missing field. Set max input to 500 to allow longer descriptions.
    seeking_desc = db.Column(db.String(500)) 
    
    #CC - Set one to many relationship between Venue and Show.
    shows = db.relationship('Show')

    def __repr__(self):
      return f'<Venue ID: {self.id} Venue: {self.name}>'

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # [DONE] implement any missing fields, as a database migration using Flask-Migrate
    
    #CC - Added to cover missing field. Used array column to store multiple genres.
    genres = db.Column(db.ARRAY(db.String))

    #CC - Added to cover missing field.
    website = db.Column(db.String(120))

    #CC - Added to cover missing field. Artist not seeking venues as default.
    seeking_venue = db.Column(db.Boolean, default=False)

    #CC - Added to cover missing field. Set max input to 500 to allow longer descriptions.
    seeking_desc = db.Column(db.String(500))

    #CC - Set one to many relationship between Artist and Show.
    shows = db.relationship('Show')

    def __repr__(self):
      return f'<Artist ID: {self.id} Artist: {self.name}>'

# [DONE] Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#CC - Added to cover missing Show model.
class Show(db.Model):
    __tablename__ = 'Show'
    #CC - id defined as primary_key.
    id = db.Column(db.Integer, primary_key=True)

    #CC - venue_id used to store venues from Venue model. Nullable set to false to ensure value is stored.
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    #CC - artist_id used to store artists from Artist model. Nullable set to false to ensure value is stored.
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

    #CC - start_time used to store start time for shows within Show model. Nullable set to false to ensure value is stored.
    start_time = db.Column(db.DateTime, nullable=False)


#----------------------------------------------------------------------------#
# Filters - DONE CC - No changes made to starter code.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers - DONE CC - No changes made to starter code.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues - DONE
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # [DONE] replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  #CC - Fetch venues data
  venues = Venue.query.order_by(Venue.name).all()

  #CC - Loops venues and appends upcoming shows.
  for venue in venues:
      
      venue_data.append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': venue.num_upcoming_shows
      })

  #CC - Show venues after appending data.
  return render_template('pages/venues.html', venues=venues);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # [DONE] implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  #CC - Fetch user's search term from form.
  term = request.form.get('search_term', '')

  #CC - Compare user's search term against list of venues. ilike used to ensure it is case-insensitive.
  result = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  
  #CC - Show a response of results and result data from above.
  response={
    #CC - Show total count of results.
    "count": len(result),
    #CC - Show result data.
    "data": result
    }

  #CC - Show search results for venue search.
  return render_template('pages/search_venues.html', results=response, search_term=term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # [DONE] replace with real venue data from the venues table, using venue_id
  
  #CC - Fetch single venue_id.
  venue = Venue.query.get(venue_id)

  #CC - Fetch list of shows for the venue using join query. Order by show start time.
  shows = Venue.query.join(Show, Show.venue_id == Venue.id).join(Artist, Artist.id == Show.artist_id).add_columns(Show.start_time.label('start_time'), Artist.id.label(
        'artist_id'), Artist.name.label('artist_name')).filter(Venue.id == venue_id).order_by(Show.start_time.desc()).all()
  
  #CC - Set variable for datetime to be used in past/upcoming shows check next.
  now = datetime.now()

  #CC - Set upcoming shows value = 0
  upcoming_shows = []

  upcoming_shows_count = 0

  #CC - Set past shows value = 0
  past_shows = []

  past_shows_count = 0

  #CC - Set count for past and upcoming shows for venue.
  for show in shows:
    if show.start_time < now:
      #CC - Increases past shows count by 1 if show.start time is less than now variable. Then appends this.
      past_shows_count = venue.past_shows_count + 1

      past_shows.append(show)

    if show.start_time > now:
      #CC - Increases upcoming shows count by 1 if show.start time is greater than now variable. Then appends this.
      upcoming_shows_count = venue.upcoming_shows_count + 1

      upcoming_shows.append(show)
      
  #CC - Show venue page for given venue_id
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue - DONE
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  #CC - Show blank venue form for new venue.
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

  

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # [DONE]: insert form data as a new Venue record in the db, instead
  # [DONE]: modify data to be the data object returned from db insertion

  form = VenueForm()
  #CC - Set error variable to False as default.
  error = False

  #CC - Try to add new venue with data from Form
  try:
    venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      genres=form.genres.data,
      website=form.website.data,
      seeking_talent=form.seeking_talent.data,
      seeking_desc=form.seeking_desc.data
    )
    #CC - Commit new venue to database.
    db.session.add(venue)
    db.session.commit()
  except:
    #CC - Rollback new venue if error occured.
    error = True
    db.session.rollback()
  finally:
    #CC - Close database connection.
    db.session.close()

  #CC - Display error message to user.
  if error:
    flash('An error occured when listing' + request.form['name'] + '.')
    abort(400)
  else:
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # [DONE]: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  #CC - Return to home page.
  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # [DONE]: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  #CC - Set error variable to False as default.
  error = False

  #CC - Try to delete venue from database.
  try:
    #CC - Fetch venue_id.
    venue = Venue.query.get(venue_id)

    #CC - Commit venue deletion.
    db.session.delete(venue)
    db.session.commit()
  except:

    #CC - Rollback venue deletion if error occured.
    error = True
    db.session.rollback()
  finally:

    #CC - Close database connection.
    db.session.close()

  if error:
    #CC - Display error message to user.
    flash('An error occured when deleting' + request.form['name'] + '.')
    abort(400)
  else:
    #CC - Display success message to user.
    flash('Venue ' + request.form['name'] + ' was successfully deleted!')

  #CC - Return to home page.
  return render_template('pages/home.html')

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  #CC - Not completed.

#  Artists - DONE
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # [DONE]: replace with real data returned from querying the database
  #CC - Fetch all Artists from database. Order alphabetically.
  data =  Artist.query.order_by(Artist.name).all()

  #CC - Show Artists page with list of all Artists from database.
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # [DONE]: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  #CC - Reverse code from Venue search app route.
  #CC - Fetch user's search term from form.
  term = request.form.get('search_term', '')

  #CC - Compare user's search term against list of Artists. ilike used to ensure it is case-insensitive.
  result = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  
  #CC - Show a response of results and result data from above.
  response={
    #CC - Show total count of results.
    "count": len(result),
    #CC - Show result data.
    "data": result
    }
  
  #CC - Show search results for artist search.

  return render_template('pages/search_artists.html', results=response, search_term=term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # [DONE] replace with real venue data from the venues table, using venue_id
  
  #CC - Reverse code from Venue id app route.

  #CC - Fetch single Artist_id.
  artist = Artist.query.get(venue_id)

  #CC - Fetch list of shows for the Artist using join query. Order by show start time.
  shows = Artist.query.join(Show, Show.artist_id == Artst.id).join(Venue, Venue.id == Show.artist_id).add_columns(Show.start_time.label('start_time'), Artist.id.label(
        'artist_id'), Artist.name.label('artist_name')).filter(Artist.id == Artist_id).order_by(Show.start_time.desc()).all()
  
  #CC - Set variable for datetime to be used in past/upcoming shows check next.
  now = datetime.now()

  #CC - Set past shows value = 0
  past_shows = []
  past_shows_count = 0

  #CC - Set upcoming shows value = 0
  upcoming_shows = []
  upcoming_shows_count = 0


  #CC - Set count for past and upcoming shows for Artist.
  for show in shows:
    if show.start_time < now:
      #CC - Increases past shows count by 1 if show.start time is less than now variable. Then appends this.
      past_shows.append(show)

      past_shows_count = artist.past_shows_count + 1

    if show.start_time > now:
      #CC - Increases past shows count by 1 if show.start time is greater than now variable. Then appends this.
      upcoming_shows.append(show)

      upcoming_shows_count = artist.upcoming_shows_count + 1

  #CC - Show venue page for given venue_id
  return render_template('pages/show_artist.html', artist=artist)

#  Update - DONE
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  #CC - Fetch Artist form
  form = ArtistForm()

  #CC - Set Artist ID
  artist = Artist.query.get(artist_id)

  #CC - Fetch Artist data
  form.name.data=artist.name
  form.city.data=artist.city
  form.state.data=artist.state
  form.phone.data=artist.phone
  form.image_link.data=artist.image_link
  form.facebook_link.data=artist.facebook_link
  form.genres.data=artist.genres
  form.website.data=artist.website
  form.seeking_venue=artist.seeking_venue
  form.seeking_desc=artist.seeking_desc

  # [DONE]: populate form with fields from artist with ID <artist_id>
  #CC - Load edit artist page with artist id and artist data
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # [DONE] take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  #CC - Fetch Artist form
  form = ArtistForm()

  #CC - Set error to false by default
  error = False

  
  try:
    #CC - replace Artist values with form values
    artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      genres=form.genres.data,
      website=form.website.data,
      seeking_venue=form.seeking_venue.data,
      seeking_desc=form.seeking_desc.data
    )
    #CC - Add new artist values to database
    db.session.add(artist)

    #CC - Commit new artist values to database
    db.session.commit()
  except:

    #CC - If error then rollback new values to database
    error = True
    db.session.rollback()
  finally:
    #CC - Close database connection
    db.session.close()

  if error:
    #CC - If error then display error message.
    flash('An error occured when editing' + request.form['name'] + '.')
    abort(400)
  else:
    #CC - Otherwise display successful message
    flash('Artist ' + request.form['name'] + ' was successfully edited!')

  #CC - Redirect user to artist page with newly updated values
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  #CC - Fetch Venue form
  form = VenueForm()

  #CC - Set Venue ID
  venue = Venue.query.get(venue_id)

  #Fetch Venue data from form
  form.name.data=venue.name
  form.city.data=venue.city
  form.state.data=venue.state
  form.phone.data=venue.phone
  form.image_link.data=venue.image_link
  form.facebook_link.data=venue.facebook_link
  form.genres.data=venue.genres
  form.website.data=venue.website
  form.seeking_artist=venue.seeking_artist
  form.seeking_desc=venue.seeking_desc

  # [DONE]: populate form with values from venue with ID <venue_id>
  #CC - Load edit venue page with venue id and venue data
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  #CC - Fetch Venue form
  form = VenueForm()

  #CC - Set error to false by default
  error = False

  try:
    #CC - replace venue values with form values
    venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      genres=form.genres.data,
      website=form.website.data,
      seeking_artist=form.seeking_artist.data,
      seeking_desc=form.seeking_desc.data
    )
    #CC - Add new venue values to database
    db.session.add(venue)

    #CC - Commit new venue values to database
    db.session.commit()
  except:

    #CC - If error then rollback new values to database
    error = True
    db.session.rollback()

  finally:
    #CC - Close database connection
    db.session.close()

  if error:
    #CC - If error then display error message.
    flash('An error occured when editing' + request.form['name'] + '.')
    abort(400)
  else:
    #CC - Otherwise display successful message
    flash('Venue ' + request.form['name'] + ' was successfully edited!')

  #CC - Redirect user to venue page with newly updated values
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist - DONE
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():

  
  form = ArtistForm()
  #CC - Show blank artist form for new artist.
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # [DONE]: insert form data as a new Venue record in the db, instead
  # [DONE]: modify data to be the data object returned from db insertion

  form = ArtistForm()

  #CC - Set error variable to False as default.
  error = False

  
  try:
    #CC - Try to add new venue with data from Form
    artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      genres=form.genres.data,
      website=form.website.data,
      seeking_venue=form.seeking_venue.data,
      seeking_desc=form.seeking_desc.data
    )
    #CC - Commit new artist to database.
    db.session.add(venue)
    db.session.commit()
  except:
    #CC - Rollback new artist if error occured.
    error = True
    db.session.rollback()
  finally:
    #CC - Close database connection.
    db.session.close()

  #CC - Display error message to user.
  if error:
    flash('An error occured when listing' + request.form['name'] + '.')
    abort(400)
  else:
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
 
  # [DONE]: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  #CC - Return to home page.
  return render_template('pages/home.html')


#  Shows - DONE
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # [DONE]: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  #CC - Fetch list of shows using join query. Order by show start time.
  shows = Show.query.join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id).add_columns(Show.venue_id, Show.artist_id, Venue.name.label(
        'venue_name'), Artist.name.label('artist_name'), Show.start_time).order_by(Show.start_time.desc()).all()

  #CC - Show shows page with list of all shows.
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()

  #CC - Show blank show form for new show.
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  form = ShowForm()

  #CC - Set error variable to False as default.
  error = False

  
  try:
    #CC - Try to add new show with data from Form
    show = Show(venue_id=form.venue_id.data, artist_id=form.artist_id.data, start_time=form.start_time.data)
    #CC - Commit new show to database.
    db.session.add(show)
    db.session.commit()
  except:
    #CC - Rollback new show if error occured.
    error = True
    db.session.rollback()
  finally:
    #CC - Close database connection.
    db.session.close()

  if error:
    #CC - Display error message to user.
    flash('An error occured when listing new show.')
    abort(400)
  else:
  # on successful db insert, flash success
    flash('Show was successfully listed!')
 
  # [DONE]: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  #CC - Return to home page.

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch. - DONE
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

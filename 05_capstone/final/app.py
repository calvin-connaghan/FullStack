import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth, get_token_auth_header


def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  #CC - after_request decorator setup to allow GET, POST, PATCH, DELETE and OPTIONS methods.
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  #CC - Movie endpoints.

  #CC - Endpoint created to handle GET requests for movies. GET method not specified as default method is GET.
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(jwt):

    movies = Movies.query.order_by(Movies.id).all()

    if movies == []:
      abort(404)

    movie_format = [movie.format() for movie in movies]

    return jsonify({
      "success": True,
      "movies": movie_format
      })

  #CC - Endpoint created to handle DELETE requests for movies. DELETE method specified.
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(token, movie_id):
    
    movie = Movies.query.get(movie_id)
      
    try:
      movie.delete()
      
      return jsonify({
        'success': True,
        'delete': movie_id
        })

    except:
      abort(404)

  #CC - Endpoint created to handle POST requests for new movies. POST method specified.
  @app.route('/movies', methods=["POST"])
  @requires_auth('post:movies')
  def create_movie(jwt):

    body = request.get_json()
    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)
    
    try:
      movie = Movies(title=new_title, release_date=new_release_date)
      movie.insert()
      movies = Movies.query.order_by(Movies.id).all()
      movie_format = [movie.format() for movie in movies]
      
      return jsonify({
        "success": True,
        "movies": movie_format
        })

    except:
      abort(422)

  #CC - Endpoint created to handle PATCH requests for movies. PATCH method specified.
  @app.route('/movies/<id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def edit_movie(jwt, movie_id):

    movie = Movies.query.get(movie_id)

    try:
      body = request.get_json()
      movie.title = body.get('title', None)
      movie.release_date = body.get('release_date', None)
      movie.update()
      movies = Movies.query.order_by(Movies.id).all()
      movie_format = [movie.format() for movie in movies]
      
      return jsonify({
        'success': True,
        'movies': movie_format
        })
    
    except:
      abort(404)

  #CC - Actor endpoints.

  #CC - Endpoint created to handle GET requests for actors. GET method not specified as default method is GET.
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(jwt):
    
    actors = Actors.query.order_by(Actors.id).all()

    if actors == []:
      abort(404)

    actor_format = [actor.format() for actor in actors]

    return jsonify({
      "success": True,
      "actors": actor_format
      })

  #CC - Endpoint created to handle DELETE requests for actors. DELETE method specified.
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(token, actor_id):
    
    actor = Actors.query.get(actor_id)
      
    try:
      actor.delete()
      
      return jsonify({
        'success': True,
        'delete': actor_id
        })

    except:
      abort(404)

  #CC - Endpoint created to handle POST requests for new actors. POST method specified.
  @app.route('/actors', methods=["POST"])
  @requires_auth('post:actors')
  def create_actor(jwt):

    body = request.get_json()
    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)
    
    try:
      actor = Actors(name=new_name, age=new_age, gender=new_gender)
      actor.insert()
      actors = Actors.query.order_by(Actors.id).all()
      actor_format = [actor.format() for actor in actors]
      
      return jsonify({
        "success": True,
        "actors": actor_format
        })
      
    except:
      abort(422)

  #CC - Endpoint created to handle PATCH requests for actors. PATCH method specified.
  @app.route('/actors/<id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def edit_actor(jwt, actor_id):

    actor = Actors.query.get(actor_id)

    try:
      body = request.get_json()
      actor.name = body.get('name', None)
      actor.age = body.get('age', None)
      actor.gender = body.get('gender', None)
      actor.update()
      actors = Actors.query.order_by(Actors.id).all()
      actor_format = [actor.format() for actor in actors]
      
      return jsonify({
        'success': True,
        'actors': actor_format
        })
    
    except:
      abort(404)

  #CC - Error Handling

  #CC - 400 Error code handler created. 
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad request."
      }), 400

  #CC - 404 Error code handler created. 
  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Resource not found."
      }), 404

  #CC - 422 Error code handler created. 
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable."
      }), 422

  #CC - Auth Error code handler created. 
  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
      "success": False, 
      "error": error.status_code,
      "message": error.error
      }), 401


  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
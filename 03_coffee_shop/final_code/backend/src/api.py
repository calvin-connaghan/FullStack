import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
[DONE] uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''

## CC - Drop db and recreate db.
db_drop_and_create_all()

## ROUTES
'''
[DONE] implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

#CC - Endpoint created to handle GET requests for drinks. GET method not specified as default method is GET.
@app.route('/drinks')
def retrieve_drinks():

    drinks = Drink.query.all()

    try:
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in drinks]
            })
    except:
        abort(404)

'''
[DONE] implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

#CC - Endpoint created to handle GET requests for drinks-detail. GET method not specified as default method is GET.
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drinks_detail(jwt):

    drinks = Drink.query.all()

    try:
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
            })
    except:
        abort(404)

'''
[DONE] implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
#CC - Endpoint created to handle POST requests for new drinks. POST method specified.
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):

    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)

    try:
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
            })
    except:
        abort(404)

'''
[DONE] implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

#CC - Endpoint created to handle PATCH requests for drinks. PATCH method specified.
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(jwt, id):

    drink = Drink.query.get(id)

    try:

        body = request.get_json()
        title = body.get('title')
        recipe = body.get('recipe')

        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
            })
    except:
        abort(404)

'''
[DONE] implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

#CC - Endpoint created to handle DELETE requests for drinks. DELETE method specified.
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    
    try:
        
        drink = Drink.query.get(drink_id)
        drink.delete()
        
        return jsonify({
        'success': True,
        'delete': drink_id,
        })
          
    except:
        abort(404)

## Error Handling
'''
Example error handling for unprocessable entity
'''

'''
[DONE] implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
[DONE] implement error handler for 404
    error handler should conform to general task above 
'''

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
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Not found."
                    }), 404

#CC - 422 Error code handler created. 
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "Unprocessable."
                    }), 422

'''
[DONE] implement error handler for AuthError
    error handler should conform to general task above 
'''

#CC - Auth Error code handler created. 
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error
                    }), 401
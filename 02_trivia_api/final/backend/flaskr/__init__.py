import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  [DONE] Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  'CC - CORS setup, allowed * for origins.
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  [DONE] Use the after_request decorator to set Access-Control-Allow
  '''

  'CC - after_request decorator setup to allow GET, POST, PATCH, DELETE and OPTIONS methods.
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

  '''
  [DONE] Create an endpoint to handle GET requests for all available categories.
  '''

  'CC - Endpoint created to handle GET requests for categories. GET method not specified as default method is GET.
  @app.route('/categories')
  def retrieve_categories():
    selection = Category.query.order_by(Category.id).all()

    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })


  '''
  [DONE] Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). 
  This endpoint should return a list of questions, number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  'CC - Endpoint created to handle GET requests for questions. GET method not specified as default method is GET.
  @app.route('/questions')
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    categories = Category.query.order_by(Category.id).all()

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all())
      'categories': {category.id: category.type for category in categories}
    })

  '''
  [DONE] Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  'CC - Endpoint created to handle DELETE requests for questions. DELETE method specified.
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

    if question is None:
      abort(404)
            
      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'deleted': question_id,
      'questions': current_questions,
      'total_questions': len(Question.query.all())
    })
        
    except:
      abort(422)

  '''
  [DONE] Create an endpoint to POST a new question, which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  'CC - Endpoint created to handle POST requests for questions. POST method specified.
  @app.route('/questions', methods=['POST'])
  def create_question(question_id):
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category' None)
    new_difficulty = body.get('rating', None)

    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'created': question_id,
      'questions': current_questions,
      'total_questions': len(Question.query.all())
    })
        
    except:
      abort(422)

  '''
  [DONE] Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  'CC - Endpoint created to handle POST (search) requests for questions. POST method specified.
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', None)
    
    try:
      question = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      current_questions = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all())
    })
        
    except:
      abort(404)

  '''
  [DONE] Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  'CC - Endpoint created to handle GET requests for questions based on category. GET method not specified as default method is GET.
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_based_on_category(category_id):
    
    try:
      selection = Question.query.filter(Question.category == category_id).all()
      current_questions = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection)
      'category': category_id}
    })

    except:
      abort(404)

  '''
  [DONE] Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  'CC - Endpoint created to handle POST requests to play the quiz. POST method specified.
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    
    try:
      body = request.get_json()
      quiz_category = body.get('quiz_category')
      previous_questions = body.get('previous_questions')

      if ( quiz_category['id']):
        questions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.notin_((previous_questions))).all()
      
      else:
        questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
      
      if len(questions) > 0:
        quiz_questions = questions[random.randrange(0, len(questions))].format()
        
      return jsonify({
        'success': True,
        'question': quiz_questions
      })
        
    except:
      abort(422)

  '''
  [DONE] Create error handlers for all expected errors including 404 and 422. 
  '''

  'CC - 400 Error code handler created. 
  @app.errorhandler(400)
    def bad_request(error):

      return jsonify({
          'success': False, 
          'error': 400,
          'message': 'Bad request.'
      }), 400

  'CC - 404 Error code handler created. 
  @app.errorhandler(404)
    def not_found(error):

      return jsonify({
          'success': False, 
          'error': 404,
          'message': 'Not found.'
      }), 404

  'CC - 422 Error code handler created. 
  @app.errorhandler(422)
    def unprocessable(error):

      return jsonify({
          'success': False, 
          'error': 422,
          'message': 'Unprocessable.'
      }), 422

  return app

    
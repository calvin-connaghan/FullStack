import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://calvo@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    [DONE] Write at least one test for each test for successful operation and for expected errors.
    """

    #CC - test created for retrieve_categories.
    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    #CC - test created for retrieve_categories_failure.
    def test_retrieve_categories_failure(self):
        res = self.client().get('/categories/120')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')


    #CC - test created for retrieve_questions.
    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    #CC - test created for retrieve_questions_failure.
    def test_retrieve_questions_failure(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    #CC - test created for delete_question.
    def test_delete_question(self):
        res = self.client().delete('/questions/9')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    #CC - test created for delete_question_failure.
    def test_delete_question_failure(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable.')

    #CC - test created for add_question.
    def test_add_question(self):
        test_question = {'question': 'test question', 'answer': 'test answer', 'category': '1', 'difficulty': '1'}
        res = self.client().post('/questions', json=test_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    #CC - test created for add_question_failure.
    def test_add_question_failure(self):
        test_question = {'question': 'test question', 'answer': 'test answer', 'category': '1', 'difficulty': '1'}
        res = self.client().post('/questions/create', json=test_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    #CC - test created for search_questions.
    def test_search_questions(self):
        test_search = {'searchTerm': 'a'}
        res = self.client().post('/questions/search', json=test_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    #CC - test created for search_questions_failure.
    def test_search_questions_failure(self):
        test_search = {'searchTerm': 'a'}
        res = self.client().post('/questions/', json=test_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    #CC - test created for retrieve_questions_based_on_category.
    def test_retrieve_questions_based_on_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['category'])

    #CC - test created for retrieve_questions_based_on_category_failure.
    def test_retrieve_questions_based_on_category_failure(self):
        res = self.client().get('/categories/a/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    #CC - test created for play_quiz.
    def test_play_quiz(self):
        test_question = {'quiz_category': {'type': 'Entertainment', 'id': 5},'previous_questions': []}
        res = self.client().post('/quizzes', json=test_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    #CC - test created for play_quiz_failure.
    def test_play_quiz_failure(self):
        test_question = {'quiz_category': {'type': 'Entertainment', 'id': 5}}
        res = self.client().post('/quizzes', json=test_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable.')

    #CC - test created for 404 error code handler.
    def test_not_found(self):
        res = self.client().get('/categories/12345')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
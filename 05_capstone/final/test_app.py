import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZQSEpUNlJtLUh6NlYyblA4c0lCVSJ9.eyJpc3MiOiJodHRwczovL2Nvbm5hZ2MuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNTY1MmUxZjgzYWRkMDA2NzFiNGE3ZSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTYwMjY3MDk4MCwiZXhwIjoxNjAyNzU3MzgwLCJhenAiOiJBdGVSbTBncFFydXgzdW1TemxvWEFSSzBvaTNKRlZhQiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.TY7VyjnWlDPWSW_X2X_VwsDBFaspKxSit__GaR9PiwWyt6AevirgDgww-9zhCG1-nuTm1Dz1twQ5f9i1hyt10sUQ29o9bzBYX0JDKJ4jTgFgJtx5czQ3PteaP1dp0Sk5xlrle8C7BFXKB0Rxc69znlE6aV_7XtW9y_-bJ2COJxB03l71bXjUlSP9dBAUfBx0-kE9BRQ8RuEbHYAMP2KV9FF3PUcURrS5fnTSY7JJx3K4OHtMmrDGyoF9-Xdyw8XKu6aw8d0q_DcBugvS0C0Gyu65i6QP8ZHGn7jCzm8gFySuCb0FjjyMU9828bKQWsm3fxEQkQjj6HIEqeAWMy26gg'
        DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZQSEpUNlJtLUh6NlYyblA4c0lCVSJ9.eyJpc3MiOiJodHRwczovL2Nvbm5hZ2MuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNTY1MmE2NDJlMzQ1MDA2ZGI0MDkzZiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTYwMjY3OTI4NCwiZXhwIjoxNjAyNzY1Njg0LCJhenAiOiJBdGVSbTBncFFydXgzdW1TemxvWEFSSzBvaTNKRlZhQiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.pDb4A5vSdiW8tE8ENP6KxIz5X9r-t4AkEAV9fAlQqBe3vgxaX5GD-OBxrc_5khCAadBgwIwq28NQTxR215wJh7GN_yI6F6l9_45esgy_zreRB_sCMJEvWTkxpnnTCO4HuqWFMP994SPEpOfMnIGJnl-Ii2cgumkfFsXQIfwxFWzjUar2gFKUyBlGp45v3wrV14nhe_FYvxFz_JMgQfd7PDNbi2SNLVikYCHaWtLM0rOOEw5RpzzRPJJHUtgLOAtig_f2IVedIQiX6vhhwQgeJtDjtGYoOCyiEpMhK6LWASdIwU2ETdW4EizzyD5OAlke0c8FylsiKv2PNQMpEJz60g'
        PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZQSEpUNlJtLUh6NlYyblA4c0lCVSJ9.eyJpc3MiOiJodHRwczovL2Nvbm5hZ2MuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmODYyZmM2YjU4NDZmMDA3NTE1MWY1ZiIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTYwMjY3OTM3MCwiZXhwIjoxNjAyNzY1NzcwLCJhenAiOiJBdGVSbTBncFFydXgzdW1TemxvWEFSSzBvaTNKRlZhQiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.h5DOheIWzecQQGQnlrp_Dvw9Aso1acHmn20HeuHGkUDNWVSwiqTyEwX2ILy9LQy1FVTjXZkhfyS0_7tuR0oHgu8z67Ih9j3pev36MYTRw--dF4AB8XzS5DHYjMF4QLGo-vurUOR4x3SabqM89dZogMulelHSrZnBDweDFRKN5wze5Pd6HCE7J8QMXv8EZhj_XSNZiiqMXbiMZqVZ_QUJ_ajPAFLPHG0xPGrbN9IIC-uhHEHlWAAcjB_RLMc5X2h0Z3Q_0Si3jXCka8tBAGyymz_xIgbw2j2GNB6gi76uvUagosXB8FHkx0xHjKlkhsd0sp1whgG45euom4gXgepkbQ'
        
        self.token_assistant = {'Content-Type': 'application/json', 'Authorization': ASSISTANT_TOKEN}
        self.token_director = {'Content-Type': 'application/json', 'Authorization': DIRECTOR_TOKEN}
        self.token_producer = {'Content-Type': 'application/json', 'Authorization': PRODUCER_TOKEN}
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency"
        self.database_path = "postgres://calvo@localhost:5432/agency"

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

    #CC - Movie endpoints.

    #CC - test created for get_movies.
    def test_get_movies(self):
        movie = Movies(title='Uncut Gems', release_date='09-01-19 12:00 pm')
        movie.insert()
        res = self.client().get('/movies', headers=self.token_producer)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(data['movies'])

    #CC - test created for get_movies failure.
    def test_get_movies_fail(self):
        res = self.client().get('/movies')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    #CC - test created for delete_movie.
    def test_delete_movie(self):
        movie = Movies(title='Uncut Gems', release_date='09-01-19 12:00 pm')
        movie.insert()
        movie_id = movie.id
        res = self.client().delete('/movies/'+str(movie_id)+'', headers=self.token_producer)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(data['delete'])

    #CC - test created for delete_movie failure.
    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/123456', headers=self.token_producer)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    #CC - test created for create_movie.
    def test_create_movie(self):
        res = self.client().post('/movies', headers=self.token_producer, json={'title': 'Good Time', 'release_date': '08-11-17 12:00 pm'})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(data['movies'])

    #CC - test created for create_movie failure.
    def test_create_movie_fail(self):
        res = self.client().post('/movies', headers=self.token_assistant, json={'title': 'Good Time', 'release_date': '08-11-17 12:00 pm'})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    #CC - test created for edit_movie.
    def test_edit_movie(self):
        movie = Movies(title='Mid80s', release_date='10-01-18 12:00 pm')
        movie.insert()
        movie_id = movie.id
        res = self.client().patch('/movies/'+str(movie_id) + '', headers=self.token_director, json={'title': 'Mid90s', 'release_date': '10-01-18 12:00 pm'})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(data['movies'])

    #CC - test created for edit_movie failure.
    def test_edit_movie_fail(self):
        movie = Movies(title='Mid80s', release_date='10-01-18 12:00 pm')
        movie.insert()
        movie_id = movie.id
        res = self.client().patch('/movies/'+str(movie_id) + '', headers=self.token_assistant, json={'title': 'Mid90s', 'release_date': '10-01-18 12:00 pm'})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(data['movies'])

    #CC - Actor endpoints.

    #CC - test created for get_actors.
    def test_get_actors(self):
        actor = Actors(name='Robert Pattison', age=34, gender='Male')
        actor.insert()
        res = self.client().get('/actors', headers=self.token_producer)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(data['actors'])

    #CC - test created for get_actors failure.
    def test_get_actors_fail(self):
        res = self.client().get('/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    #CC - test created for delete_actor.
    def test_delete_actor(self):
        actor = Actors(name='Robert Pattison', age=34, gender='Male')
        actor.insert()
        actor_id = actor.id
        res = self.client().delete('/actors/'+str(actor_id)+'', headers=self.token_producer)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(data['delete'])

    #CC - test created for delete_actor failure.
    def test_delete_actor_fail(self):
        res = self.client().delete('/actors/123456', headers=self.token_producer)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    #CC - test created for create_actor.
    def test_create_actor(self):
        res = self.client().post('/actors', headers=self.token_producer, json={'name': 'Benny Safdie', 'age': 34, 'gender': 'Male'})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(data['actors'])

    #CC - test created for create_actor failure.
    def test_create_actor_fail(self):
        res = self.client().post('/actors', headers=self.token_assistant, json={'name': 'Benny Safdie', 'age': 34, 'gender': 'Male'})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    #CC - test created for edit_actor.
    def test_edit_actor(self):
        actor = Actors(name='Taliah Webster', age=22, gender='Male')
        actor.insert()
        actor_id = actor.id
        res = self.client().patch('/actors/'+str(actor_id)+'', headers=self.token_director, json={'name': 'Taliah Webster', 'age': 22, 'gender': 'Female'})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(data['actors'])

    #CC - test created for edit_actor failure.
    def test_edit_actor_fail(self):
        actor = Actors(name='Taliah Webster', age=22, gender='Male')
        actor.insert()
        actor_id = actor.id
        res = self.client().patch('/actors/'+str(actor_id)+'', headers=self.token_assitant, json={'name': 'Taliah Webster', 'age': 22, 'gender': 'Female'})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)
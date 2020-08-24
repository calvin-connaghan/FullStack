# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Documentation

At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

Error Handling
Errors are returned as JSON objects in the following format:
{
    "success": False, 
    "error": 400,
    "message": "Bad request."
}
The API will return three error types when requests fail:

400: Bad Request.
404: Not Found.
422: Unprocessable.

Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions/id'
POST '/questions'
POST '/questions/search'
GET '/categories/id/questions'
POST '/quizzes'

GET '/categories'
Returns a success value and a list of categories.

Sample: curl http://127.0.0.1:5000/categories

GET '/questions'
Returns a success value, list of questions, total number of questions and category for each question.
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: curl http://127.0.0.1:5000/questions

DELETE '/questions/id'
Deletes the question of the given ID if it exists. Returns a success value, the id of the deleted question, list of questions and total number of questions.

Sample: curl -X DELETE http://127.0.0.1:5000/questions/1

POST '/questions'
Creates a new question using the submitted question, answer, category and rating. Returns a success value, the id of the created question, list of questions and total number of questions.

Sample: curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"question":"Who was the first British team to win the European Cup?", "answer":"Celtic FC", "category":"Sports", "rating":"5"}'

POST '/questions/search'
Creates a new search using the submitted search term. Returns a success value, list of questions containing the search term and total number of questions. Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "World Cup"}'

GET '/categories/id/questions'
Returns a success value, list of questions within a specified category, total number of questions within specified category and specified category id.
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: curl localhost:5000/categories/1/questions

POST '/quizzes'
Creates a list of random questions from a specifed category whilst also excluding previous questions. Returns a success value and list of randomized questions from specified category.

Sample: curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2], "quiz_category": {"type": "Sports", "id": "1"}}' http://localhost:5000/quizzes


## Testing

In order to run tests navigate to the backend folder and run the following commands:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.
All tests are kept in that file and should be maintained as updates are made to app functionality.

## Authors

Calvin Connaghan

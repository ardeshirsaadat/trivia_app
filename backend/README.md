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

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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

# API DOCUMENTAION

## Base URL:

This app can be run locally.

## Authentication:

This version of the app does not require authentication or API keys.

## Error Handling:

Errors are returned as JSON objects in the following format:

```
{
    'success':False,
    'error':404,
    'message':'The server can not find the requested resource'
}
```

The API will return three error types when requests fail

```
404: 'The server can not find the requested resource'
422: 'The request was well-formed but was unable to be followed due to semantic errors'
500:  'The server has encountered a situation it does not know how to handle'
```

## Resource Endpoints

```
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Request Arguments: page parameter as an URL query
- Returns:
{

  'success':True,
  'questions': an array of questions' objects,
  'total_questions': an integer ,
  'categories': a dictionary of with id as key and type as value,
  'current_category': an array of current categories
  }

DELETE '/questions/<question_id>'
- Deletes the specified question form database
- Request Arguments: question id
- Returns:
{
  'success':True
}

POST '/questions'
- Adds a new question object to database
- Request Arguments: a dictionary as following specifications {'question':string,'answer':string,'difficulty':int,'category':int}
- Returns:
{
  'success':True
}

POST '/questions/search'
- Searches for existing questions of specified keyword
- Request Arguments: a dictionary as following specifications {'searchTerm':any}
- Returns:
{
  'success':True,
  'questions':an array of question objects,
  'total_questions':an integer,
  'currentCategory': an array of current categories
}

GET '/categories/<category_id>/questions'
- Request Arguments: category id
- Returns:
{
  'success':True,
  'questions': an array of question objects based on specified category,
  'total_questions': number of questions in that category,
  'currnet_category': an array of current category
}

POST '/quizzes'
- Request Arguments: a dictionary as following specifications {'previous_questions':array of question ids,'quiz_category':{'id':an integer representing category id, 'type':a string representing category's name}}
- Returns:
{
  'success':True,
  'question':a question object
}

```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

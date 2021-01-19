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
        self.database_path = "postgres://{}:{}@{}/{}".format(
    'postgres', '16760', 'localhost:5432', self.database_name)
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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])

    def test_422_get_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)    

    def test_questions_post(self):
        res = self.client().post('/questions',json={'question':'why','answer':'yes','difficulty':3,'category':1})
        data = json.loads(res.data)

        self.assertTrue(data['success'])

    
    def test_500_questions_post(self):
        res = self.client().post('/questions',json={'question':'why','answer':'yes','difficulty':3,'category':"fd"})
        data = json.loads(res.data)

        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],500)    

    def test_search_post(self):
        res = self.client().post('/questions/search',json={'searchTerm':'organ'})
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_search_post(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404) 

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])  

    def test_404_get_question_by_category(self):
        res = self.client().get('/categories/20/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404) 

    def test_quizzes_post(self):
        res = self.client().post('/quizzes',json={'previous_questions':[],'quiz_category':{'id':1}})
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_404_quizzes_post(self):
        res = self.client().post('/quizzes',json={'previous_questions':[1,5],'quiz_category':[{'id':20}]})
        data = json.loads(res.data)

        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404) 

         
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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
     
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    
    def test_new_question(self):
        new_question = {
            'question':'what is faviorate subjuct',
            'answer': 'cumputer',
            'difficulty':2 ,
            'category':1 }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_new_question_fail(self):
        new_question = {
            'question':'',
            'answer': '',
            'difficulty':2 ,
            'category':1 
            }
        res = self.client().post('/categories', json= new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/1')
    #     data = json.loads(res.data)
    #     question = Question.query.get(1)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 1)
    #     self.assertEqual(question, None)

    def test_get_questions_by_categories(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_search_question_with_result(self):
        search_term =  {'searchTerm':'name'}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(len(data['questions']),2)

    def test_search_question_without_result(self):
        search_term =  {'searchTerm':'almuteri'}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'],0)
        self.assertEqual(len(data['questions']),0)

    def test_search_question_fail(self):
        search_term =  {}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad Request')

    def test_play_quezzies(self):
        requst_data={
            "previous_questions":[],
            "quiz_category":{"type":"Science","id":3}}
        res = self.client().post('/quizzes', json=requst_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(len(data['question']))

    def test_play_quezzies_fail(self):
        requst_data={
             "previous_questions":[]}
            
        res = self.client().post('/quizzes', json=requst_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    

    


        

if __name__ == "__main__":
    unittest.main()
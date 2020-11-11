import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category



def create_app(test_config=None):
 
  app = Flask(__name__)
  setup_db(app)
  
  
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    return response


  
  @app.route('/categories')
  def get_categories():
    category=Category.query.all()
    data={}
    for i in category:
      print(i)
      data[i.id]=i.type
    
    return jsonify({
          'success': True,
          'categories':data
        })


  @app.route('/questions',methods=['POST'])
  def post_question():
    data=request.get_json()
    new_question= Question(question=data['question'],
      answer=data['answer'],
      difficulty=data['difficulty'],
      category=data['category'])
    new_question.insert()
    
    print(data)
    return jsonify({
          'success': True,
          'questions':new_question.id
        })

      
    

  
  @app.route('/questions')
  def get_question():
    questions  = Question.query.all()
    page = request.args.get('page', 1, type=int)
    limit= request.args.get('limit', 10, type=int)
    offset=(page-1) * limit
    end=offset + limit
    data=[qu.format()for qu in questions]
    

    qustion_paginate= data[offset:end]
    print(data)

    category=Category.query.all()
    data1={}
    for i in category:
      data1[i.id]=i.type
    

    return jsonify({
          'success': True,
          'questions': qustion_paginate,
          'totalQuestions':len(questions),
          'categories': data1,
          'currentCategory': None
           
        })

      
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    question = Question.query.get(id)
    question.delete()
    

    return jsonify({
    'success': True,
    'delated':question.id
        })

  @app.route('/questions/search', methods=['POST'])
  def search_question():  
    data=request.get_json()
    search_term=data['searchTerm']
    result =Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    page = request.args.get('page', 1, type=int)
    limit= request.args.get('limit', 10, type=int)
    offset=(page-1) * limit
    end=offset + limit
    data=[qu.format()for qu in result]
    qustion_paginate= data[offset:end]
   
    return jsonify({
            'success': True,
            'questions': qustion_paginate,
            'totalQuestions':len(result),
            'currentCategory':None
            
          })
    
 

  
  
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_categories(category_id):
    question=Question.query.filter_by(category=category_id).all()
    page = request.args.get('page', 1, type=int)
    limit= request.args.get('limit', 10, type=int)
    offset=(page-1) * limit
    end=offset + limit
    data=[qu.format()for qu in question]
    qustion_paginate= data[offset:end]
    return jsonify({
          'success': True,
          'questions': qustion_paginate,
          'total_questions': len(question),
          'current_category':category_id
        })

  @app.route('/quizzes',methods=['POST'])
  def play_quizzes(): 
    data=request.get_json()
    previous_questions= data['previous_questions']
    category= data['quiz_category']
    

    question=Question.query.filter_by(category=category['id']).all()
    print(question)
    new_question=question[random.randrange(0,len(question),1)]

  
    if new_question in previous_questions:
       new_question=question[random.randrange(0,len(question),1)]
    print(new_question)
     

    


    return jsonify({
      'success': True,
      'currentQuestion':new_question.format()
        })

 
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method Not Allowed"
        }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400
        
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": " Internal Server Error"
        }), 500
  return app

    
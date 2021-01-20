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
    CORS(app)

    '''
  @DONE: Set up CORS. Allow '*' for origins.
   Delete the sample route after completing the TODOs
  '''

    '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
  @DONE:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET', 'POST'])
    def get_categories():
        if request.method == 'POST':
            abort(404)
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)
        formated_categories = [category.format() for category in categories]
        print(formated_categories)
        return jsonify({
            'success': True,
            'categories': {
                       category['id']: category['type'] for category in formated_categories}})

    '''
  @DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            page = request.args.get('page', 1, type=int)
            questions = Question.query.order_by(Question.id).all()
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions_formatted = [question.format() for question in questions]
            questions_per_page = questions_formatted[start:end]
            if len(questions_per_page) == 0:
                abort(404)
            categories = [
                category.format() for category in Category.query.order_by(
                    Category.id).all()]
            # print(questions_formatted)
            return jsonify({
                'success': True,
                'questions': questions_per_page,
                'total_questions': len(questions),
                'categories': {int(category['id']): category['type'] for category in categories},
                'current_category': [question['category'] for question in questions_per_page]
            })
        except BaseException:
            abort(422)

    '''
  @DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question_to_delete = Question.query.get(question_id)
            if not (question_to_delete):
                abort(404)
            question_to_delete.delete()
            return jsonify({
                'success': True,
                'ID': question_id
            })
        except BaseException:
            abort(422)
    '''
  @DONE:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def post_qustion():
        try:
            data = request.get_json()
            question = data.get('question', None)
            answer = data.get('answer', None)
            difficulty = data.get('difficulty', None)
            category = data.get('category', None)
            question_object = Question(
                question, answer, category, difficulty)
            question_object.insert()
            return jsonify({
                'success': True
            })
        except BaseException:
            abort(500)
    '''
  @DONE:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_qustion():
        try:
            data = request.get_json()
            search_term = data.get('searchTerm', None)
            results = Question.query.filter(
                Question.question.ilike('%{}%'.format(search_term))).all()
            results_formated = [question.format()
                                for question in results]

            return jsonify({
                'success': True,
                'questions': results_formated,
                'total_questions': len(results),
                'currentCategory': [question['category'] for question in results_formated]})
        except BaseException:
            abort(404)
    '''
  @DONE:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            questions_formatted = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': questions_formatted,
                'total_questions': len(questions),
                'currnet_category': Category.query.get(category_id).type
            })
        except BaseException:
            abort(404)
    '''
  @DONE:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def get_next_question():
        try:
            data = request.get_json()
            previous_questions = data.get('previous_questions', None)
            quiz_category = data.get('quiz_category', None)
            if quiz_category['id'] == 0:
                questions_by_category = Question.query.all()
            else:
                questions_by_category = Question.query.filter(
                    Question.category == int(quiz_category['id']))
            questions_by_category_formatted = [
                question.format() for question in questions_by_category]
            next_question = random.choice(questions_by_category_formatted)
            while next_question['id'] in previous_questions:
                next_question = random.choice(questions_by_category_formatted)
                if len(previous_questions) == len(
                        questions_by_category_formatted):
                    next_question = False
                    break

            return jsonify({
                'success': True,
                'question': next_question
            })
        except BaseException:
            abort(404)
    '''
  @DONE:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'The server can not find the requested resource'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'The request was well-formed but was unable to be followed due to semantic errors'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'The server has encountered a situation it does not know how to handle'
        }), 500
    return app

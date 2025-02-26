from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity
from models import Admin, User, Subject, Chapter, Quiz, Question, Score
from extensions import db
from datetime import datetime
from auth import admin_required, user_required

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            access_token = create_access_token(
                identity=admin.id,
                expires_delta=False,
                additional_claims={'role': 'admin'}
            )
            return {'access_token': access_token, 'role': 'admin'}, 200

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(
                identity=user.id,
                additional_claims={'role': 'user'}
            )
            return {'access_token': access_token, 'role': 'user'}, 200

        return {'message': 'Invalid credentials'}, 401

class UserRegistrationResource(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400
        
        dob = datetime.strptime(data['dob'], '%d/%m/%Y').date()
        user = User(
            username=data['username'],
            full_name=data['full_name'],
            qualification=data['qualification'],
            dob=dob
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        return {'message': 'User created successfully'}, 201

class SubjectResource(Resource):
    @admin_required
    def post(self):
        data = request.get_json()
        subject = Subject(
            name=data['name'],
            description=data['description']
        )
        db.session.add(subject)
        db.session.commit()
        return {'message': 'Subject created successfully'}, 201

    @admin_required
    def get(self):
        subjects = Subject.query.all()
        return {
            'subjects': [{
                'id': subject.id,
                'name': subject.name,
                'description': subject.description,
                'chapters': [{
                    'id': chapter.id,
                    'name': chapter.name,
                    'description': chapter.description
                } for chapter in subject.chapters]
            } for subject in subjects]
        }


# TODO: Add a chapter resource too where admin can create new chapters and the user can view the chapters

class QuizResource(Resource):
    @admin_required
    def post(self):
        data = request.get_json()
        quiz = Quiz(
            chapter_id=data['chapter_id'],
            date_of_quiz=datetime.strptime(data['date_of_quiz'], '%Y-%m-%d %H:%M:%S'),
            time_duration=data['time_duration']
        )
        db.session.add(quiz)
        db.session.commit()
        return {'message': 'Quiz created successfully'}, 201

    @user_required
    def get(self, quiz_id=None):
        if quiz_id is not None:
            # Handle user request for specific quiz
            if not get_jwt_identity():
                return {'message': 'Unauthorized'}, 401
                
            quiz = Quiz.query.get_or_404(quiz_id)
            num_questions = len(quiz.questions)
            question_ids = [question.id for question in quiz.questions]
            return {
                'id': quiz.id,
                'chapter_id': quiz.chapter_id,
                'date_of_quiz': quiz.date_of_quiz.isoformat(),
                'time_duration': str(quiz.time_duration),
                'num_questions': num_questions,
                'question_ids': question_ids
            }
        else:
            # Handle admin request for all quizzes
            if not get_jwt_identity():
                return {'message': 'Unauthorized'}, 401
                
            quizzes = Quiz.query.all()
            return {
                'quizzes': [{
                    'id': quiz.id,
                    'chapter_id': quiz.chapter_id,
                    'date_of_quiz': quiz.date_of_quiz.isoformat(),
                    'time_duration': str(quiz.time_duration)
                } for quiz in quizzes]
            }


class QuestionResource(Resource):
    @admin_required
    def post(self):
        data = request.get_json()
        question = Question(
            quiz_id=data['quiz_id'],
            question_statement=data['question_statement'],
            option1=data['option1'],
            option2=data['option2'],
            option3=data['option3'],
            option4=data['option4'],
            correct_answer=data['correct_answer']
        )
        db.session.add(question)
        db.session.commit()
        return {'message': 'Question created successfully'}, 201

    @user_required
    def get(self, question_id):
        question = Question.query.get_or_404(question_id)
        return {
            'id': question.id,
            'quiz_id': question.quiz_id,
            'question_statement': question.question_statement,
            'options': [question.option1, question.option2, question.option3, question.option4]
        }

class ScoreResource(Resource):
    @user_required
    def get(self):
        user_id = get_jwt_identity()
        scores = Score.query.filter_by(user_id=user_id).all()
        return {
            'scores': [{
                'quiz_id': score.quiz_id,
                'total_score': score.total_score,
                'timestamp': score.time_stamp_of_attempt.isoformat()
            } for score in scores]
        }

class SubmitAnswersResource(Resource):
    @user_required
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        quiz_id = data['quiz_id']
        answers = data['answers']

        quiz = Quiz.query.get_or_404(quiz_id)
        if not quiz.is_open_today():
            return {'message': 'Quiz is not open today'}, 400
        
        if Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first():
            return {'message': 'Answers already submitted for this quiz'}, 400

        total_score = 0
        for answer in answers:
            question = Question.query.get_or_404(answer['question_id'])
            if question.correct_answer == answer['selected_option']:
                total_score += 1

        score = Score(
            user_id=user_id,
            quiz_id=quiz_id,
            total_score=total_score
        )
        db.session.add(score)
        db.session.commit()
        return {'message': 'Answers submitted successfully', 'total_score': total_score}, 201
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
    def get(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        return {
            'id': quiz.id,
            'chapter_id': quiz.chapter_id,
            'date_of_quiz': quiz.date_of_quiz.isoformat(),
            'time_duration': str(quiz.time_duration)
        }

class ScoreResource(Resource):
    @user_required
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        score = Score(
            user_id=user_id,
            quiz_id=data['quiz_id'],
            total_score=data['total_score']
        )
        db.session.add(score)
        db.session.commit()
        return {'message': 'Score recorded successfully'}, 201

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
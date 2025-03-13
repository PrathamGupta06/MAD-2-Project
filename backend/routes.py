from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity
from models import Admin, User, Subject, Chapter, Quiz, Question, Score
from extensions import db
from datetime import datetime
from auth import admin_required, user_required
from extensions import cache
from celery_tasks import generate_admin_report

class GenerateAdminReport(Resource):
    @admin_required
    def post(self):
        task = generate_admin_report.delay()
        return {'message': 'Export started. You will receive an email once it\'s complete.'}, 200

# TODO: Add the batch job, implement the search functionality for user, Code cleanup and add more caching and invalidation.

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
                expires_delta=False,
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
        cache.delete_memoized(SubjectResource.get)
        return {'message': 'Subject created successfully'}, 201

    @admin_required
    @cache.memoize()
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

    @admin_required
    def put(self, subject_id):
        subject = Subject.query.get_or_404(subject_id)
        data = request.get_json()
        subject.name = data['name']
        subject.description = data['description']
        db.session.commit()
        cache.delete_memoized(SubjectResource.get)
        return {'message': 'Subject updated successfully'}, 200

    @admin_required
    def delete(self, subject_id):
        subject = Subject.query.get_or_404(subject_id)
        db.session.delete(subject)
        db.session.commit()
        return {'message': 'Subject deleted successfully'}, 200

class ChapterResource(Resource):
    @admin_required
    def post(self):
        data = request.get_json()
        chapter = Chapter(
            name=data['name'],
            description=data['description'],
            subject_id=data['subject_id']
        )
        db.session.add(chapter)
        db.session.commit()
        cache.delete_memoized(SubjectResource.get)
        cache.delete_memoized(ChapterResource.get)
        return {'message': 'Chapter created successfully'}, 201

    @admin_required
    def put(self, chapter_id):
        chapter = Chapter.query.get_or_404(chapter_id)
        data = request.get_json()
        chapter.name = data['name']
        chapter.description = data['description']
        db.session.commit()
        cache.delete_memoized(SubjectResource.get)
        cache.delete_memoized(ChapterResource.get)
        return {'message': 'Chapter updated successfully'}, 200
    
    @admin_required
    def delete(self, chapter_id):
        chapter = Chapter.query.get_or_404(chapter_id)
        db.session.delete(chapter)
        db.session.commit()
        cache.delete_memoized(SubjectResource.get)
        cache.delete_memoized(ChapterResource.get)
        return {'message': 'Chapter deleted successfully'}, 200
    
    @user_required
    @cache.memoize()
    def get(self, chapter_id):
        chapter = Chapter.query.get_or_404(chapter_id)
        return {
            'id': chapter.id,
            'name': chapter.name,
            'description': chapter.description,
            'subject_id': chapter.subject_id
        }

class QuizResource(Resource):
    @admin_required
    def put(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        data = request.get_json()
        quiz.chapter_id = data['chapter_id']
        quiz.date_of_quiz = datetime.strptime(data['date_of_quiz'], '%Y-%m-%d')
        quiz.time_duration = data['time_duration']
        db.session.commit()
        return {'message': 'Quiz updated successfully'}, 200

    @admin_required
    def delete(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        cache.delete_memoized(QuizResource.get)
        cache.delete_memoized(QuizzesResource.get)
        return {'message': 'Quiz deleted successfully'}, 200

    @user_required
    @cache.memoize()
    def get(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        num_questions = len(quiz.questions)
        question_ids = [question.id for question in quiz.questions]
        return {
            'id': quiz.id,
            'chapter_id': quiz.chapter_id,
            'chapter_name': quiz.chapter.name,
            'subject_id': quiz.chapter.subject_id,
            'subject_name': quiz.chapter.subject.name,
            'date_of_quiz': quiz.date_of_quiz.isoformat(),
            'time_duration': str(quiz.time_duration),
            'num_questions': num_questions,
            'question_ids': question_ids
        }


class QuizzesResource(Resource):
    @admin_required
    def post(self):
        data = request.get_json()
        quiz = Quiz(
            chapter_id=data['chapter_id'],
            date_of_quiz=datetime.strptime(data['date_of_quiz'], '%Y-%m-%d'),
            time_duration=data['time_duration']
        )
        db.session.add(quiz)
        db.session.commit()
        cache.delete_memoized(QuizResource.get)
        cache.delete_memoized(QuizzesResource.get)
        return {'message': 'Quiz created successfully'}, 201

    @user_required
    @cache.memoize()
    def get(self):
        quizzes = Quiz.query.all()
        quizzes_data = []
        for quiz in quizzes:
            quiz_data = {
                'id': quiz.id,
                'chapter_id': quiz.chapter_id,
                'chapter_name': quiz.chapter.name,
                'subject_id': quiz.chapter.subject_id,
                'subject_name': quiz.chapter.subject.name,
                'date_of_quiz': quiz.date_of_quiz.isoformat(),
                'time_duration': str(quiz.time_duration)
            }
            questions = Question.query.filter_by(quiz_id=quiz.id).all()
            # Add the quesion_id, question_statement 
            quiz_data['questions'] = [{
                'id': question.id,
                'question_statement': question.question_statement
            } for question in questions]
            quizzes_data.append(quiz_data)
        return {'quizzes': quizzes_data}


class QuestionResource(Resource):
    @admin_required
    def post(self):
        data = request.get_json()

        if data['correct_answer'] not in (1, 2, 3, 4):
            return {'message': 'Invalid Correct Answer (Select one of 1, 2, 3, 4).'}, 400

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

    @admin_required
    @cache.memoize()
    def get(self, question_id):
        question = Question.query.get_or_404(question_id)
        return {
            'id': question.id,
            'quiz_id': question.quiz_id,
            'question_statement': question.question_statement,
            'options': [question.option1, question.option2, question.option3, question.option4],
            'correct_answer': question.correct_answer
        }
    
    @admin_required
    def put(self, question_id):
        question = Question.query.get_or_404(question_id)
        data = request.get_json()
        question.question_statement = data['question_statement']
        question.option1 = data['option1']
        question.option2 = data['option2']
        question.option3 = data['option3']
        question.option4 = data['option4']
        question.correct_answer = data['correct_answer']
        db.session.commit()
        return {'message': 'Question updated successfully'}, 200

    @admin_required
    def delete(self, question_id):
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return {'message': 'Question deleted successfully'}, 200

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
            question = Question.query.filter_by(id=answer['question_id'], quiz_id=quiz_id).first()
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



class UpcomingQuizzesResource(Resource):
    @user_required
    def get(self):
        user_id = get_jwt_identity()
        current_time = datetime.now()
        all_quizzes = Quiz.query.all()
        
        today_quizzes = Quiz.query.filter(
            Quiz.date_of_quiz == current_time.date(),
        ).all()

        upcoming_quizzes = Quiz.query.filter(
            Quiz.date_of_quiz > current_time.date(),
        ).order_by(Quiz.date_of_quiz.asc()).all()
       
        today_quizzes_response = [
            {
                'id': quiz.id,
                'chapter_name': quiz.chapter.name,
                'subject_name': quiz.chapter.subject.name,
                'date_of_quiz': quiz.date_of_quiz.isoformat(),
                'time_duration': str(quiz.time_duration),
                'num_questions': len(quiz.questions),
                'attempted': True if Score.query.filter_by(quiz_id = quiz.id, user_id = user_id).all() else False
            }
            for quiz in today_quizzes
        ]
        
        upcoming_quizzes_response = [
            {
                'id': quiz.id,
                'chapter_name': quiz.chapter.name,
                'subject_name': quiz.chapter.subject.name,
                'date_of_quiz': quiz.date_of_quiz.isoformat(),
                'time_duration': str(quiz.time_duration),
                'num_questions': len(quiz.questions),
                'attempted': True if Score.query.filter_by(quiz_id = quiz.id, user_id = user_id).all() else False
            }
            for quiz in upcoming_quizzes
        ]
        return {
            'today_quizzes': today_quizzes_response,
            'upcoming_quizzes': upcoming_quizzes_response
        }


class QuizQuestionsResource(Resource):
    @user_required
    @cache.memoize()
    def get(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        return {
            'id': quiz.id,
            'chapter_name': quiz.chapter.name,
            'subject_name': quiz.chapter.subject.name,
            'time_duration': quiz.time_duration,
            'questions': [{
                'id': question.id,
                'question_statement': question.question_statement,
                'options': [
                    question.option1,
                    question.option2,
                    question.option3,
                    question.option4
                ]
            } for question in quiz.questions]
        }

class UserSummaryResource(Resource):
    @user_required
    def get(self):
        user_id = get_jwt_identity()

        subjects = Subject.query.all()
        subject_data = []

        for subject in subjects:
            quiz_count = sum(len(chapter.quizzes) for chapter in subject.chapters)

            attempted_count = db.session.query(Score).join(Quiz).join(Chapter) \
                .filter(Score.user_id == user_id) \
                .filter(Chapter.subject_id == subject.id).count()

            subject_data.append({
                'subject_name': subject.name,
                'total_quizzes': quiz_count,
                'attempted_quizzes': attempted_count
            })

        current_year = datetime.now().year
        monthly_data = [
            {
                'month': datetime(current_year, month, 1).strftime('%B'),
                'attempts': db.session.query(Score)
                .filter(Score.user_id == user_id)
                .filter(db.extract('month', Score.time_stamp_of_attempt) == month)
                .filter(db.extract('year', Score.time_stamp_of_attempt) == current_year)
                .count()
            }
            for month in range(1, 13)
        ]

        return {
            'subject_data': subject_data,
            'monthly_data': monthly_data
        }


class AdminSummaryResource(Resource):
    @admin_required
    @cache.memoize()
    def get(self):
        subjects = Subject.query.all()
        subject_stats = []

        for subject in subjects:
            quiz_ids = [quiz.id for chapter in subject.chapters for quiz in chapter.quizzes]

            if not quiz_ids:
                subject_stats.append({
                    'subject_name': subject.name,
                    'average_score': 0,
                    'total_attempts': 0,
                    'total_questions': 0
                })
                continue

            scores = Score.query.filter(Score.quiz_id.in_(quiz_ids)).all()
            total_questions = db.session.query(db.func.count(Question.id)) \
                .filter(Question.quiz_id.in_(quiz_ids)).scalar() or 0

            average_score = round(sum(score.total_score for score in scores) / len(scores), 2) if scores else 0

            subject_stats.append({
                'subject_name': subject.name,
                'average_score': average_score,
                'total_attempts': len(scores),
                'total_questions': total_questions
            })

        total_attempts_per_subject = [
            {
                'subject_name': subject.name,
                'total_attempts': db.session.query(Score)
                .join(Quiz).join(Chapter)
                .filter(Chapter.subject_id == subject.id)
                .count()
            }
            for subject in subjects
        ]

        total_users = User.query.count()
        total_attempts = Score.query.count()

        return {
            'subject_stats': subject_stats,
            'quiz_attempts_per_subject': total_attempts_per_subject,
            'user_stats': {
                'total_users': total_users,
                'total_attempts': total_attempts
            }
        }

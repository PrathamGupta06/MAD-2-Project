from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from extensions import db, jwt, cache, mail, excel
from celery_factory import celery_init_app
from config import Config
from routes import (
    LoginResource, UserRegistrationResource, 
    SubjectResource, QuizResource, QuizzesResource, ScoreResource, SubmitAnswersResource, QuestionResource,
    ChapterResource, UserQuizzesResource, QuizQuestionsResource, UserSummaryResource, AdminSummaryResource
)

from routes import GenerateAdminReport
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    excel.init_excel(app)
    app.cache = cache
    
    api = Api(app)
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(UserRegistrationResource, '/api/register')
    api.add_resource(SubjectResource, '/api/subjects', '/api/subjects/<int:subject_id>')
    api.add_resource(QuizResource, '/api/quizzes/<int:quiz_id>')
    api.add_resource(QuizzesResource, '/api/quizzes')
    api.add_resource(UserQuizzesResource, '/api/user/quizzes')
    api.add_resource(ScoreResource, '/api/scores')
    api.add_resource(SubmitAnswersResource, '/api/submit-answers')
    api.add_resource(QuestionResource, '/api/questions', '/api/questions/<int:question_id>')
    api.add_resource(ChapterResource, '/api/chapters', '/api/chapters/<int:chapter_id>')
    api.add_resource(QuizQuestionsResource, '/api/user/quizQuestions/<int:quiz_id>')
    api.add_resource(UserSummaryResource, '/api/user/summary')
    api.add_resource(AdminSummaryResource, '/api/admin/summary')
    api.add_resource(GenerateAdminReport, '/api/admin/generate_report')

    with app.app_context():
        from models import Admin
        db.create_all()
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin')
            admin.set_password(os.environ.get('ADMIN_PASSWORD'))
            db.session.add(admin)
            db.session.commit()    
    return app

app = create_app()
celery_app =  celery_init_app(app)
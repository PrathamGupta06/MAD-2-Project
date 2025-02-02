from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from extensions import db, jwt
from config import Config
from routes import (
    LoginResource, UserRegistrationResource, 
    SubjectResource, QuizResource, ScoreResource
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    
    api = Api(app)
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(UserRegistrationResource, '/api/register')
    api.add_resource(SubjectResource, '/api/subjects')
    api.add_resource(QuizResource, '/api/quizzes', '/api/quizzes/<int:quiz_id>')
    api.add_resource(ScoreResource, '/api/scores')

    with app.app_context():
        from models import Admin
        db.create_all()
        admin = Admin.query.filter_by(username='admin@quizmaster.com').first()
        if not admin:
            admin = Admin(username='admin@quizmaster.com')
            admin.set_password('adminpass')
            db.session.add(admin)
            db.session.commit()    
    return app
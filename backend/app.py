from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from extensions import db, jwt
from config import Config
from routes import LoginResource, UserRegistrationResource

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    
    api = Api(app)
    api.add_resource(LoginResource, '/login')
    api.add_resource(UserRegistrationResource, '/register')

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
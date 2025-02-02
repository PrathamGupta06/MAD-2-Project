from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from redis import Redis
from celery import Celery
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()
redis = Redis()
celery = Celery()

from app.models import Admin

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    with app.app_context():
        db.create_all()
        admin = Admin.query.filter_by(username='admin@quizmaster.com').first()
        if not admin:
            admin = Admin(username='admin@quizmaster.com')
            admin.set_password('adminpass')
            db.session.add(admin)
            db.session.commit()
    
    return app
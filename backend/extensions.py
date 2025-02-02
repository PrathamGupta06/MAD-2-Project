from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from redis import Redis
from celery import Celery

db = SQLAlchemy()
jwt = JWTManager()
redis = Redis()
celery = Celery()

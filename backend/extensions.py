from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_mail import Mail
import flask_excel as excel

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
mail = Mail()
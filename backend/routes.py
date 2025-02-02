from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from models import Admin, User
from extensions import db
from datetime import datetime

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
import jwt
from os import environ
from datetime import datetime, timedelta
from flask_restful import (Resource, request)
from models.user import UserModel, UserSchema
from webargs.flaskparser import use_args
from webargs import fields
from flask import flash, redirect, url_for

user_args ={'username': fields.Str(required=True), 'password': fields.Str(required=True), 'name': fields.Str(), 'email': fields.Str()}


class UserRegister(Resource):

    @use_args(user_args, locations=('json', 'form'))
    def post(self, user_args):
        user_schema=UserSchema()
        user_data = user_args

        error = user_schema.validate(user_data)
        if error:
            if request.content_type == 'application/x-www-form-urlencoded':
                for message, message_value in error.items():
                    error_message = ''.join(message_value)
                return redirect(url_for('signup', error=error_message))
            else:
                return {'status': 'fail', 'message': error}, 400
        username_exist = UserModel.filter_and_find_first(username=user_data['username'])
        if username_exist:
            if request.content_type == 'application/x-www-form-urlencoded':
                return redirect(url_for('signup', error='username already exist'))
            else:
                return {'status': 'fail', 'message': 'username already exist'}, 409

        email_exist = UserModel.filter_and_find_first(email=user_data['email'])
        if email_exist:
            if request.content_type == 'application/x-www-form-urlencoded':
                return redirect(url_for('signup', error='email already exist'))
            else:
                return {'status': 'fail', 'message': 'email already exist'}, 409

        new_user = UserModel(**user_data)
        new_user.save_to_db()
        new_user_json = user_schema.dump(new_user).data
        if request.content_type == 'application/x-www-form-urlencoded':
            return redirect(url_for('index', error=request.args.get('error')))
        else:
            return {'status': 'success', 'data': new_user_json}, 201

    @staticmethod
    def put():
        user_schema=UserSchema(partial={'password'})
        user_data = request.get_json()
        error = user_schema.validate(user_data)
        if error:
            return {'status': 'fail','message': error}, 400
        user_result = UserModel.filter_and_find_first(username=user_data['username'])

        if user_result:
            user_result.email = user_data['email']
            user_result.name = user_data['name']
            user_result.save_to_db()
            new_user_json = user_schema.dump(user_result).data
            return {'status': 'success', 'data': new_user_json}, 200
        return {'status': 'fail', 'message': 'user does not exist'}, 404


class UserLogin(Resource):
    @use_args(user_args, locations=('json', 'form'))
    def post(self, args):
        user_schema=UserSchema(partial=('name', 'email'))
        user_data = args
        error = user_schema.validate(user_data)

        if error:
            if request.content_type == 'application/x-www-form-urlencoded':
                return redirect(url_for('index', error=error.get('username')))
            else:
                return {'status': 'fail', 'message': error}, 400
        user_exist = UserModel.filter_and_find_first(username=user_data['username'].lower(),
                                                     password=user_data['password'].lower())
        if not user_exist:
            if request.content_type == 'application/x-www-form-urlencoded':
                return redirect(url_for('index', error='username and password does not exist'))
            else:
                return {'status': 'fail', 'message': 'username and password does not exist'}, 409
        user_data_json = UserSchema(exclude=('password',)).dump(user_exist).data
        key = environ.get('SECRET')
        payload = {'user': user_data_json, 'exp': datetime.utcnow() + timedelta(minutes=30)}
        token = jwt.encode(payload, key=key, algorithm='HS256').decode('utf-8')
        if request.content_type == 'application/x-www-form-urlencoded':
            return redirect(url_for('books_page'))
        else:
            return {'status': 'success', 'data': {'token': str(token), 'user': user_data_json}}







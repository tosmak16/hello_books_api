from flask_restful import Resource, request
from models.user import UserModel, UserSchema


class UserRegister(Resource):

    @staticmethod
    def post():
        user_schema=UserSchema()
        user_data = request.get_json()

        error = user_schema.validate(user_data)
        if error:
            return {'status': 'fail','message': error}, 400
        username_exist = UserModel.filter_and_find_first(username=user_data['username'])
        if username_exist:
            return {'status': 'fail', 'message': 'username already exist'}, 409

        email_exist = UserModel.filter_and_find_first(email=user_data['email'])
        if email_exist:
            return {'status':'fail', 'message': 'email already exist'}, 409

        new_user = UserModel(**user_data)
        new_user.save_to_db()
        new_user_json = user_schema.dump(new_user).data
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



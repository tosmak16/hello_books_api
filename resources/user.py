from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="username is required")
    parser.add_argument('password', type=str, required=True, help='password is required')
    parser.add_argument('email', type=str, required=True, help='email is required')
    parser.add_argument('name', type=str, required=True, help='name is required')

    @staticmethod
    def post():
        user_data = UserRegister.parser.parse_args()
        user_result = UserModel.find_by_name(user_data['username'])

        if user_result:
            return {'message': 'username already exist'}, 400

        new_user = UserModel(**user_data)
        new_user.save_to_db()
        return new_user.json(), 201

    @staticmethod
    def put():
        user_data = UserRegister.parser.parse_args()
        user_result = UserModel.find_by_name(user_data['username'])

        if user_result:
            user_result.email = user_data['email']
            user_result.name = user_data['name']
            user_result.save_to_db()
            return user_result.json(), 200

        new_user = UserModel(**user_data)
        new_user.save_to_db()
        return new_user.json(), 201


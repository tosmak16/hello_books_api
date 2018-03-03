from flask import Flask
from flask_restful import Api
from os import environ
from resources.user import UserRegister
from resources.borrowedbook import BorrowedBooks, BorrowedBooksList
from resources.book import Books, SingleBook


app = Flask(__name__, instance_relative_config=True)
api = Api(app)


api.add_resource(SingleBook, '/api/v1/books/<string:id>')
api.add_resource(Books, '/api/v1/books')
api.add_resource(UserRegister, '/api/v1/signup')
api.add_resource(BorrowedBooksList, '/api/v1/borrowedbooks')
api.add_resource(BorrowedBooks, '/api/v1/users/<string:user_id>/books')


@app.route('/')
def index():
    """
    Render a Hello World response.

    :return: Flask response
    """
    return 'Hellohgvhbjhbh World!'


if __name__ == '__main__':
    app.run(port=int(environ['PORT']))

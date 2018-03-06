from flask import Flask
from flask_restful import Api
from os import environ
from resources.user import UserRegister
from resources.borrowedbook import BorrowedBooks, BorrowedBooksList
from resources.book import Books, SingleBook
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db import db

migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    api = Api(app)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    print(environ['DATABASE_URI'])

    @app.before_first_request
    def create_tables():
        db.create_all()

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
        return 'welcome to hello books!'
    return app

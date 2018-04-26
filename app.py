from flask import Flask, render_template, request
from flask_restful import Api
from resources.user import UserRegister, UserLogin
from resources.borrowedbook import BorrowedBooks, BorrowedBooksList
from resources.book import Books, SingleBook
from flask_migrate import Migrate
from db import db
from instance.config import app_config


migrate = Migrate()


def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)

    api = Api(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.add_resource(SingleBook, '/api/v1/books/<string:id>')
    api.add_resource(Books, '/api/v1/books')
    api.add_resource(UserRegister, '/api/v1/signup')
    api.add_resource(UserLogin, '/api/v1/signin')
    api.add_resource(BorrowedBooksList, '/api/v1/borrowedbooks')
    api.add_resource(BorrowedBooks, '/api/v1/users/<string:user_id>/books')

    @app.route('/')
    def index():
        """
        Render a Hello World response.

        :return: Flask response
        """
        return render_template('index.html', error=request.args.get('error'))

    @app.route('/signup')
    def signup():
        """
        Render a Hello World response.

        :return: Flask response
        """
        return render_template('signup.html', error=request.args.get('error'))

    @app.route('/books')
    def books_page():
        """
        Render a Hello World response.

        :return: Flask response
        """
        return render_template('books.html')
    return app

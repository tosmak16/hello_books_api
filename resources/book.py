from flask_restful import Resource, reqparse

from models.book import BookModel


class Books(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('title', type=str, required=True,
                        help="title is required")
    parser.add_argument('author', type=str, required=True,
                        help='author is required')
    parser.add_argument('description', type=str,
                        required=True, help='description is required')
    parser.add_argument('image', type=str, required=True,
                        help='image is required')
    parser.add_argument('file', type=str, required=True,
                        help='file is required')
    parser.add_argument('category', type=str, required=True,
                        help='category is required')
    parser.add_argument('isbn', type=int, required=True,
                        help='isbn is required')

    @staticmethod
    def post():
        book_data = Books.parser.parse_args()
        book_result = BookModel.find_by_isbn(book_data['isbn'])
        if book_result:
            return {'message': '{} already exist'.format(book_data['title'])}
        new_book = BookModel(**book_data)
        new_book.save_book()
        return new_book.json(), 201

    @staticmethod
    def get():
        return {'books': [book.json() for book in BookModel.query.all()]}


class SingleBook(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('title', type=str, required=True,
                        help="title is required")
    parser.add_argument('author', type=str, required=True,
                        help='author is required')
    parser.add_argument('description', type=str,
                        required=True, help='description is required')
    parser.add_argument('image', type=str, required=True,
                        help='image is required')
    parser.add_argument('file', type=str, required=True,
                        help='file is required')
    parser.add_argument('category', type=str, required=True,
                        help='category is required')
    parser.add_argument('isbn', type=int, required=True,
                        help='isbn is required')

    @staticmethod
    def get(id):
        book_result = BookModel.find_by_id(id)
        if book_result:
            return book_result.json()
        return {'message': 'book does not exist'}, 404

    @staticmethod
    def put(id):
        book_data = SingleBook.parser.parse_args()
        book_result = BookModel.find_by_id(id)
        if book_result:
            book_result.title = book_data['title']
            book_result.author = book_data['author']
            book_result.description = book_data['description']
            book_result.image = book_data['image']
            book_result.file = book_data['file']
            book_result.category = book_data['category']
            book_result.save_book()
            return book_result.json()
        return {'message': 'book does not exist'}, 404

    @staticmethod
    def delete(id):
        book_result = BookModel.find_by_id(id)
        if book_result:
            book_result.delete_book()
            return {'message': '{} has been deleted'.format(book_result.title)}, 200

        return {'message': 'book does not exist'}, 404

from flask_restful import Resource, reqparse, request
from datetime import date
from models.borrowedbook import BorrowedBooksModel
from models.book import BookModel
from models.user import UserModel


class BorrowedBooks(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('book_id', type=str, required=True, help='book_id is required')

    # handles user borrow books request
    @staticmethod
    def post(user_id):
        borrowed_book_data = BorrowedBooks.parser.parse_args()
        borrowed_book_result = BorrowedBooksModel.verify_if_borrowed(user_id, borrowed_book_data['book_id'])

        if not BookModel.find_by_id(borrowed_book_data['book_id']):
            return {'message': 'Book does not exist'}, 404
        if not UserModel.find_by_id(user_id):
            return {'message': 'Invalid user you can not borrow books'}, 403
        if borrowed_book_result:
            return {'message': 'you have borrowed this book before'}, 400
        dict_borrowed_book_data = {
            'book_id': borrowed_book_data['book_id'],
            'book_status': False,
            'borrowed_date': date.today(),
            'returned_date': ''
        }
        new_borrowed_book_data = BorrowedBooksModel(user_id=user_id, **dict_borrowed_book_data)
        new_borrowed_book_data.save_to_db()
        return new_borrowed_book_data.json(), 201

    @staticmethod
    def get(user_id):
            try:
                returned = request.args['returned']
            except:
                returned = None
            if returned:
                    un_returned_books = BorrowedBooksModel.query.filter_by(user_id=user_id, book_status=False)
                    return {'borrowed_books': [borrowed_books.json() for borrowed_books in un_returned_books]}

            borrowed_books_history = BorrowedBooksModel.query.filter_by(user_id=user_id)
            return {'borrowed_books_history': [borrowed_books.json() for borrowed_books in borrowed_books_history]}

    # handles return borrow books request
    @staticmethod
    def put(user_id):
        borrowed_book_data = BorrowedBooks.parser.parse_args()
        if not BookModel.find_by_id(borrowed_book_data['book_id']):
            return {'message': 'Book does not exist'}, 404
        if not UserModel.find_by_id(user_id):
            return {'message': 'Invalid user you can not borrow books'}, 403
        borrowed_book_result = BorrowedBooksModel.verify_if_borrowed(user_id, borrowed_book_data['book_id'])
        if not borrowed_book_result:
            return {'message': 'you need to borrow this book'}, 400
        borrowed_book_result.returned_date = date.today()
        borrowed_book_result.book_status = True
        borrowed_book_result.save_to_db()
        return borrowed_book_result.json(), 200


class BorrowedBooksList(Resource):

    @staticmethod
    def get():
        return {'all_borrowed_books': [borrowed_books.json() for borrowed_books in BorrowedBooksModel.query.all()]}


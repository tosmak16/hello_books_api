from flask_restful import Resource, request
from datetime import datetime
from models.borrowedbook import BorrowedBooksModel, BorrowedBooksSchema
from models.book import BookModel
from models.user import UserModel


class BorrowedBooks(Resource):

    # handles user borrow books request
    @staticmethod
    def post(user_id):
        borrowed_book_data = request.get_json()
        borrowed_book_schema = BorrowedBooksSchema(partial=('borrowed_date', 'returned_date', 'book_status',))
        errors = borrowed_book_schema.validate({'user_id': user_id, 'book_id': borrowed_book_data.get('book_id')})
        if errors:
            return {'status': 'fail', 'message': errors}, 400
        if not BookModel.find_by_id(borrowed_book_data['book_id']):
            return {'status': 'fail', 'message': 'Book does not exist'}, 404
        if not UserModel.find_by_id(user_id):
            return {'message': 'Invalid user you can not borrow books'}, 403
        filter_term={'user_id': user_id, 'book_id': borrowed_book_data['book_id'], 'book_status': False}
        borrowed_book_result = BorrowedBooksModel.find_first(**filter_term)
        if borrowed_book_result:
            return {'message': 'you have borrowed this book before'}, 400
        dict_borrowed_book_data = {
            'user_id': user_id,
            'book_id': borrowed_book_data['book_id'],
            'book_status': False,
            'borrowed_date': str(datetime.utcnow()),
            'returned_date': None
        }
        new_borrowed_book_data = BorrowedBooksModel(**dict_borrowed_book_data)
        new_borrowed_book_data.save_to_db()
        new_borrowed_book_data_json = BorrowedBooksSchema(many=False, exclude=('user', 'book', ))\
            .dump(new_borrowed_book_data).data
        return {'status': 'success', 'data': new_borrowed_book_data_json}, 201

    @staticmethod
    def get(user_id):
            returned = request.args.get('returned')
            borrowed_book_schema = BorrowedBooksSchema(partial=('borrowed_date', 'book_id',
                                                                'returned_date', 'book_status'))
            errors = borrowed_book_schema.validate({'user_id': user_id})
            if errors:
                return {'status': 'fail', 'message': errors}, 400
            if returned is not None and returned.upper() == 'FALSE':
                    un_returned_books = BorrowedBooksModel.filter_by(user_id=user_id, book_status=False)
                    un_returned_books_json = BorrowedBooksSchema(many=True, exclude=('user', 'book',)) \
                        .dump(un_returned_books).data
                    return {'status': 'success', 'data': un_returned_books_json}

            borrowed_books_history = BorrowedBooksModel.filter_by(user_id=user_id)
            borrowed_books_history_json = BorrowedBooksSchema(many=True, exclude=('user', 'book',)) \
                .dump(borrowed_books_history).data
            return {'status': 'success', 'data': borrowed_books_history_json}

    # handles return borrow books request
    @staticmethod
    def put(user_id):
        borrowed_book_data = request.get_json()
        borrowed_book_schema = BorrowedBooksSchema(partial=('borrowed_date', 'returned_date', 'book_status',))
        errors = borrowed_book_schema.validate({'user_id': user_id, 'book_id': borrowed_book_data.get('book_id')})
        if errors:
            return {'status': 'fail', 'message': errors}, 400
        if not BookModel.find_by_id(borrowed_book_data['book_id']):
            return {'status': 'fail', 'message': 'Book does not exist'}, 404
        if not UserModel.find_by_id(user_id):
            return {'status': 'fail', 'message': 'Invalid user you can not borrow books'}, 403
        borrowed_book_result = BorrowedBooksModel.find_first(user_id=user_id,
                                                             book_id=borrowed_book_data['book_id'], book_status=False)
        if not borrowed_book_result:
            return {'message': 'you need to borrow this book'}, 406
        borrowed_book_result.returned_date = datetime.utcnow()
        borrowed_book_result.book_status = True
        borrowed_book_result.save_to_db()
        borrowed_book_result_json = BorrowedBooksSchema(many=False, exclude=('user', 'book',)) \
            .dump(borrowed_book_result).data
        return {'status': 'success', 'data': borrowed_book_result_json}


class BorrowedBooksList(Resource):

    @staticmethod
    def get():
        all_borrowed_books=BorrowedBooksModel.fetch_all()
        all_borrowed_books_json = BorrowedBooksSchema(many=True, exclude=()) \
            .dump(all_borrowed_books).data
        return {'status': 'success', 'data': all_borrowed_books_json}



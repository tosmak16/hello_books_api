from flask_restful import Resource, request
from models.book import BookModel, BookSchema


class Books(Resource):

    @staticmethod
    def post():
        request_body = request.get_json()
        book_schema = BookSchema()
        book = book_schema.load(request_body)
        if book.errors:
            return dict(status='fail', data=book.errors), 400

        book_result = BookModel.find_by_isbn(request_body['isbn'])

        if book_result:
            return {'message': '{} already exist'.format(book.data['title'])}, 409
        new_book = BookModel(**book.data)
        new_book.save_book()
        book_data = book_schema.dump(new_book).data
        return {'status': 'success', 'book': book_data}, 201

    @staticmethod
    def get():
        books = BookModel.query.all()
        book_schema = BookSchema(many=True)
        book_data = book_schema.dump(books).data
        return {'status': 'success', 'books': book_data}


class SingleBook(Resource):

    @staticmethod
    def validate_book_id(id):
        book_schema = BookSchema(partial=True)
        return book_schema.validate(dict(id=id), partial=True)

    @staticmethod
    def get(id):
        book_schema = BookSchema(partial=True)
        is_not_valid = SingleBook.validate_book_id(id)
        if is_not_valid:
            return {'status': 'fail', 'message': 'A valid book id is required'}, 400
        book_result = BookModel.find_by_id(id)
        if book_result:
            book_data = book_schema.dump(book_result).data
            return {'status': 'success', 'books': book_data}
        return {'status': 'fail', 'message': 'book does not exist'}, 404

    @staticmethod
    def put(id):
        request_body = request.get_json()
        book_schema = BookSchema()
        book = book_schema.load(request_body)
        if book.errors:
            return dict(status='fail', data=book.errors), 400
        is_not_valid = SingleBook.validate_book_id(id)
        if is_not_valid:
            return {'status': 'fail', 'message': 'A valid book id is required'}, 400
        book_data = book.data
        book_result = BookModel.find_by_id(id)
        if book_result:
            book_result.title = book_data['title'] if book_data.get('title') else book_result.title
            book_result.author = book_data['author'] if book_data.get('author') else book_result.author
            book_result.description = book_data['description'] \
                if book_data.get('description') else book_result.description
            book_result.image = book_data['image']if book_data.get('image') else book_result.image
            book_result.file = book_data['file']if book_data.get('file') else book_result.file
            book_result.category = book_data['category']if book_data.get('category') else book_result.category
            book_result.save_book()
            updated_book_data = book_schema.dump(book_result).data
            return {'status': 'success', 'book': updated_book_data}
        return {'message': 'book does not exist'}, 404

    @staticmethod
    def delete(id):
        is_not_valid = SingleBook.validate_book_id(id)
        if is_not_valid:
            return {'status': 'fail', 'message': 'A valid book id is required'}, 400
        book_result = BookModel.find_by_id(id)
        if book_result:
            book_result.delete_book()
            return {'message': '{} has been deleted'.format(book_result.title)}, 200

        return {'message': 'book does not exist'}, 404

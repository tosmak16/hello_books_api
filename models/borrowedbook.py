from db import db


class BorrowedBooksModel(db.Model):

    __tablename__ = 'borrowedbooks'

    id = db.Column(db.Integer, primary_key=True)
    borrowed_date = db.Column(db.Integer, nullable=False)
    returned_date = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    book_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.borrowed_date = kwargs['borrowed_date']
        self.returned_date = kwargs['returned_date'] if kwargs['returned_date'] else 'null'
        self.user_id = kwargs['user_id']
        self.book_id = kwargs['book_id']
        self.book_status = kwargs['book_status']

    def json(self):
        return {
            'id': self.id, 'user_id': self.user_id,
            'borrowed_date': self.borrowed_date, 'book_status': self.book_status,
            'returned_date': self.returned_date, 'book_id': self.book_id
        }

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_book_id(cls, book_id):
        return cls.query.filter_by(book_id=book_id).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def verify_if_borrowed(cls, user_id, book_id):
        print(user_id)
        return cls.query.filter_by(user_id=user_id, book_id=book_id, book_status=False).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

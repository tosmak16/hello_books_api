from db import db
from marshmallow import Schema, fields
from models.user import UserSchema
from models.book import BookSchema


class BorrowedBooksModel(db.Model):

    __tablename__ = 'borrowedbooks'

    id = db.Column(db.Integer, primary_key=True)
    borrowed_date = db.Column(db.String(50), nullable=False)
    returned_date = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    book = db.relationship('BookModel', backref='borrowedbooks', lazy=True)
    user = db.relationship('UserModel', backref='borrowedbooks', lazy=True)
    book_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.borrowed_date = kwargs['borrowed_date']
        self.returned_date = kwargs['returned_date'] if kwargs.get('returned_date') else None
        self.user_id = kwargs['user_id']
        self.book_id = kwargs['book_id']
        self.book_status = kwargs['book_status']

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
    def find_first(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class BorrowedBooksSchema(Schema):
    borrowed_date = fields.DateTime()
    returned_date = fields.DateTime()
    book_status = fields.Boolean()
    user_id = fields.Integer(required=True, error_messages={'required': 'user_id is required'})
    book_id = fields.Integer()
    user = fields.Nested(UserSchema)
    book = fields.Nested(BookSchema)



from flask_sqlalchemy import SQLAlchemy
from db import db


class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False,)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.Integer, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    file = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(80), nullable=False)
    borrowedbooks = db.relationship('BorrowedBooksModel')

    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.author = kwargs['author']
        self.isbn = kwargs['isbn']
        self.description = kwargs['description']
        self.image = kwargs['image']
        self.file = kwargs['file']
        self.category = kwargs['category']

    def json(self):
        return {
            'title': self.title, 'author': self.author, 'image': self.image,
            'category': self.category, 'isbn': self.isbn, 'file': self.file,
            'description': self.description, 'id': self.id,
            'borrowedbooks': [borrowedbook.json() for borrowedbook in self.borrowedbooks.all()]
        }

    @classmethod
    def find_by_isbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    def save_book(self):
        db.session.add(self)
        db.session.commit()

    def delete_book(self):
        db.session.delete(self)
        db.session.commit()

from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship
from database import db_session

class BookModel(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False,)
    author = Column(String(80), nullable=False)
    isbn = Column(Integer, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    image = Column(String(100), nullable=True)
    file = Column(String(100), nullable=True)
    category = Column(String(80), nullable=False)
    borrowedbooks = relationship('BorrowedBooksModel', lazy='dynamic')

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
                'description': self.description, 'id': self.id
                }

    @classmethod
    def find_by_isbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    def save_book(self):
        db_session.add(self)
        db_session.commit()

    def delete_book(self):
        db_session.delete(self)
        db_session.commit()

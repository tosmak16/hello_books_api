from db import db
from marshmallow import Schema, fields, validate, validates, ValidationError


class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False,)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    file = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(80), nullable=False)

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.author = kwargs.get('author')
        self.isbn = kwargs.get('isbn')
        self.description = kwargs.get('description')
        self.image = kwargs.get('image')
        self.file = kwargs.get('file')
        self.category = kwargs.get('category')

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


class BookSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True, error_messages={'required': 'book title is required'})
    author = fields.String(required=True, error_messages={'required': 'author is required'})
    isbn = fields.String(required=True, error_messages={'required': 'isbn is required'})
    description = fields.String(required=True, error_messages={'required':'description is required'})
    image = fields.Url(validate=validate.URL(error='image must be a valid url'))
    file = fields.Url(validate=validate.URL(error='file must be a valid url'))
    category = fields.String(required=True, error_messages={'required': 'category is required'},
                             validate=[validate.Length(min=1, max=25,
                                                       error='book category should be in the range of 1 and 25')])

    @validates('isbn')
    def validate_isbn(self, data):
        try:
            int(data)
        except ValueError:
            raise ValidationError('isbn must be a number only')

        if len(data) > 13 or len(data) < 10:
            raise ValidationError('isbn should be in the range of 10 and 13')


from db import db
from marshmallow import Schema, fields, validates, ValidationError


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.email = kwargs['email']
        self.name = kwargs['name']


    @classmethod
    def filter_and_find_first(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class UserSchema(Schema):
    username = fields.String(required=True, error_messages={'required': 'username is required'})
    password = fields.String(required=True, error_messages={'required': 'password is required'})
    name = fields.String(required=True, error_messages={'required': 'name is required'})
    email = fields.Email(required=True, error_messages={'required': 'email is required'})

    @validates('username')
    def validate_username(self, data):
        if len(data) > 15 or len(data) < 2:
            raise ValidationError('username should be in the range of 2 and 15')

    @validates('password')
    def validate_password(self, data):
        if len(data) > 15 or len(data) < 6:
            raise ValidationError('password should be in the range of 6 and 15')

    @validates('name')
    def validate_password(self, data):
        if len(data) > 25 or len(data) < 2:
            raise ValidationError('name should be in the range of 2 and 25')

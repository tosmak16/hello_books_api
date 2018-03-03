from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship
from database import db_session



class UserModel(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)
    borrowedbooks = relationship('BorrowedBooksModel', lazy='dynamic')

    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.email = kwargs['email']
        self.name = kwargs['name']

    def json(self):
        return {'name': self.name, 'username': self.username, 'email': self.email}

    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    def save_to_db(self):
        db_session.add(self)
        db_session.commit()

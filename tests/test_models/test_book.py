from ..test_base import HelloBooksTestCase
from app import create_app, db
from models.book import BookModel
import pytest


class BooksTestCase(HelloBooksTestCase):

    def test_find_by_isbn(self):
        self.setUp
        book = BookModel()
        result = book.find_by_isbn(1)
        assert result == None

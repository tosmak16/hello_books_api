from ..test_base import HelloBooksTestCase
from models.book import BookModel



class BooksTestCase(HelloBooksTestCase):

    def test_find_by_isbn(self):
        self.setUp
        book = BookModel()
        result = book.find_by_isbn("123446567678")
        assert result == None

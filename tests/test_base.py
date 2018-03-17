import unittest
from app import create_app, db


class HelloBooksTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client

        self.app.app_context().push()
        db.create_all()

    def tearDown(self):
        self.app = create_app('testing')
        self.app.app_context().push()
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()

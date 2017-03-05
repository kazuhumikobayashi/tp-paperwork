import unittest

from application import app, db
from tests.fixture import init_data


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # creates a test client
        app.config.from_object('config.testing')
        cls.app = app.test_client()
        # propagate the exceptions to the test client
        cls.app.testing = True
        db.drop_all()
        db.create_all()
        init_data()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()

    def setUp(self):
        pass

    def tearDown(self):
        pass

import datetime
import unittest

from application import app, db


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
        cls().create_user()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_user(self):
        # self.app.post('/register', data={
        #     'user_name': '単体テスト1',
        #     'mail': 'test@test.com',
        #     'password': 'test',
        #     'password_confirmation': 'test'
        # })
        # self.app.post('/register', data={
        #     'user_name': '単体テスト2',
        #     'mail': 'test@test2.com',
        #     'password': 'test',
        #     'password_confirmation': 'test'
        # })
        # self.app.post('/register', data={
        #     'user_name': '単体テスト3',
        #     'mail': datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '@test.com',
        #     'password': 'test',
        #     'password_confirmation': 'test'
        # })
        pass

import unittest
from datetime import datetime

from application import app, db, bcrypt
from application.domain.model.user import User


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
        for num in range(12):
            user = User(
                     shain_number='test' + str(num),
                     user_name='単体テスト',
                     mail='test@test' + str(num) + '.com',
                     password=bcrypt.generate_password_hash('test'),
                     created_at=datetime.today(),
                     created_user='test',
                     updated_at=datetime.today(),
                     updated_user='test')
            db.session.add(user)
        db.session.commit()

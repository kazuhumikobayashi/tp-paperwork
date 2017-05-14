from datetime import datetime

from nose.tools import ok_
from tests import BaseTestCase

from application import db
from application.const import ClientFlag
from application.domain.model.destination import Destination
from application.domain.repository.destination_repository import DestinationRepository


class DestinationTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(DestinationTests, cls).setUpClass()

    def setUp(self):
        super(DestinationTests, self).setUp()
        self.destination_repository = DestinationRepository()

    def tearDown(self):
        super(DestinationTests, self).tearDown()

    # 宛先情報の検索画面に遷移する。
    def test_get_destination(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/destination/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_destination_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/destination/page/2')
        self.assertEqual(result.status_code, 200)

    # 宛先情報を検索する。
    def test_search_destination(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/destination/?company_id=1&destination_name=test&destination_department=test')
        self.assertEqual(result.status_code, 200)

    # 会社登録画面に遷移する。
    def test_get_destination_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/destination/create')
        self.assertEqual(result.status_code, 200)

    # 会社詳細画面に遷移する。
    def test_get_destination_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        destination = self.destination_repository.find_all()[0]

        result = self.app.get('/destination/detail/' + str(destination.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない会社の場合はnot_found
    def test_get_destination_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/destination/detail/0')
        self.assertEqual(result.status_code, 404)

    # 宛先情報を保存できる
    def test_save_destination(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        destination = self.destination_repository.find_all()[0]

        expected = '単体テスト_変更'
        destination_id = destination.id

        result = self.app.post('/destination/detail/' + str(destination_id), data={
            'company_id': destination.company_id,
            'destination_name': destination.destination_name,
            'destination_department': expected,
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/destination/detail/' + str(destination.id) in result.headers['Location'])

        destination = self.destination_repository.find_by_id(destination_id)
        actual = destination.destination_department
        self.assertEqual(actual, expected)

    # 宛先情報を削除できる
    def test_delete_destination(self):
        # 削除用の宛先を登録
        destination = Destination(
            company_id=1,
            destination_name='削除用会社',
            destination_department='削除用部署',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(destination)
        db.session.commit()

        delete_destination_id = destination.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        destination = self.destination_repository.find_by_id(delete_destination_id)

        result = self.app.get('/destination/delete/' + str(destination.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/destination' in result.headers['Location'])

        # 削除した会社が存在しないことを確認
        destination = self.destination_repository.find_by_id(delete_destination_id)
        self.assertIsNone(destination.id)

    # 存在しない会社は削除できない
    def test_delete_destination_fail(self):
        before = len(self.destination_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/destination/delete/0')
        # 削除できないことを確認
        self.assertEqual(result.status_code, 302)
        ok_('/destination' in result.headers['Location'])

        after = len(self.destination_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 宛先情報を新規登録できる
    def test_create_destination(self):
        before = len(self.destination_repository.find_all())
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/destination/create', data={
            'company_id': '1',
            'destination_name': 'test_create_destination',
            'destination_department': 'test_create_destination',
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.destination_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

from datetime import datetime

from nose.tools import ok_

from application import db
from application.domain.model.holiday import Holiday
from application.domain.repository.holiday_repository import HolidayRepository
from tests import BaseTestCase


class HolidayTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(HolidayTests, cls).setUpClass()

    def setUp(self):
        super(HolidayTests, self).setUp()
        self.holiday_repository = HolidayRepository()

    def tearDown(self):
        super(HolidayTests, self).tearDown()

    # 祝日の検索画面に遷移する。
    def test_get_holiday(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/holiday/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_holiday_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        print(self.holiday_repository.find_all())

        result = self.app.get('/holiday/page/2')
        self.assertEqual(result.status_code, 200)

    # 祝日を検索する。
    def test_search_holiday(self):
        this_year = str(datetime.today().year)

        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/holiday/?year=' + this_year)
        self.assertEqual(result.status_code, 200)

    # 祝日をブランクで検索する。
    def test_search_holiday_year_blank(self):

        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/holiday/?year=')
        self.assertEqual(result.status_code, 200)

    # 祝日登録画面に遷移する。
    def test_get_holiday_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/holiday/create')
        self.assertEqual(result.status_code, 200)

    # 祝日登録する。
    def test_create_holiday(self):
        before = len(self.holiday_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/holiday/create', data={
            'holiday': '2000/1/1',
            'holiday_name': 'テスト登録'
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.holiday_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

    # 祝日登録に失敗する
    def test_create_holiday_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/holiday/create', data={
            'holiday': '2000/3/1',
            'holiday_name': '重複テスト'
        })
        self.assertEqual(result.status_code, 302)

        before = len(self.holiday_repository.find_all())

        result = self.app.post('/holiday/create', data={
            'holiday': '2000/3/1',
            'holiday_name': '重複テスト'
        })
        self.assertEqual(result.status_code, 200)

        after = len(self.holiday_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 祝日詳細画面に遷移する。
    def test_get_holiday_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        holiday = self.holiday_repository.find_all()[0]

        result = self.app.get('/holiday/detail/' + str(holiday.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない祝日の場合はnot_found
    def test_get_holiday_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/holiday/detail/0')
        self.assertEqual(result.status_code, 404)

    # 祝日を保存できる
    def test_save_holiday(self):
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        holiday = self.holiday_repository.find_all()[0]

        expected = '単体テスト_変更'
        holiday_id = holiday.id

        result = self.app.post('/holiday/detail/' + str(holiday_id), data={
            'holiday': holiday.holiday.strftime('%Y/%m/%d'),
            'holiday_name': expected
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/holiday/detail/' + str(holiday.id) in result.headers['Location'])

        holiday = self.holiday_repository.find_by_id(holiday_id)
        actual = holiday.holiday_name
        self.assertEqual(actual, expected)

    # 祝日を削除できる
    def test_delete_holiday(self):
        # 削除用の祝日を登録
        holiday = Holiday(
            holiday='2000/4/1',
            holiday_name='削除用祝日',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(holiday)
        db.session.commit()

        delete_holiday_id = holiday.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        holiday = self.holiday_repository.find_by_id(delete_holiday_id)

        result = self.app.get('/holiday/delete/' + str(holiday.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/holiday' in result.headers['Location'])

        # 削除した祝日が存在しないことを確認
        holiday = self.holiday_repository.find_by_id(delete_holiday_id)
        self.assertIsNone(holiday.id)

    # 存在しない祝日は削除できない
    def test_delete_holiday_fail(self):
        before = len(self.holiday_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/holiday/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/holiday' in result.headers['Location'])

        after = len(self.holiday_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

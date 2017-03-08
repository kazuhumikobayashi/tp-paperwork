from datetime import datetime

from nose.tools import ok_

from application import db
from application.domain.model.calculation import Calculation
from application.domain.repository.calculation_repository import CalculationRepository
from tests import BaseTestCase


class CalculationTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(CalculationTests, cls).setUpClass()

    def setUp(self):
        super(CalculationTests, self).setUp()
        self.calculation_repository = CalculationRepository()

    def tearDown(self):
        super(CalculationTests, self).tearDown()

    # 計算式の検索画面に遷移する。
    def test_get_calculation(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/calculation/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_calculation_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/calculation/page/2')
        self.assertEqual(result.status_code, 200)

    # 計算式を検索する。
    def test_search_calculation(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/calculation/?calculation_name=test')
        self.assertEqual(result.status_code, 200)

    # 計算式登録画面に遷移する。
    def test_get_calculation_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/calculation/create')
        self.assertEqual(result.status_code, 200)

    # 計算式を登録する。
    def test_create_calculation(self):
        before = len(self.calculation_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/calculation/create', data={
            'amount': '9999',
            'formula': '1',
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.calculation_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

    # 計算式登録に失敗する。
    def test_create_calculation_fail(self):
        before = len(self.calculation_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 同じ名称のスキルは登録できない
        result = self.app.post('/calculation/create', data={
            'amount': '0',
            'formula': '1',
        })
        self.assertEqual(result.status_code, 200)

        after = len(self.calculation_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 計算式詳細画面に遷移する。
    def test_get_calculation_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        calculation = self.calculation_repository.find_all()[0]

        result = self.app.get('/calculation/detail/' + str(calculation.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない計算式の場合はnot_found
    def test_get_calculation_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/calculation/detail/0')
        self.assertEqual(result.status_code, 404)

    # 計算式を保存できる
    def test_save_calculation(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        calculation = self.calculation_repository.find_all()[0]

        expected = '10000円未満切り捨て'
        calculation_id = calculation.id

        result = self.app.post('/calculation/detail/' + str(calculation_id), data={
            'amount': '10000',
            'formula': '1',
        })
        # 計算式できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/calculation/detail/' + str(calculation.id) in result.headers['Location'])

        calculation = self.calculation_repository.find_by_id(calculation_id)
        actual = calculation.calculation_name
        self.assertEqual(actual, expected)

    # 計算式を削除できる
    def test_delete_calculation(self):
        # 削除用の計算式を登録
        calculation = Calculation(
            calculation_name='100000円未満切り捨て',
            amount=100000,
            formula=1,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(calculation)
        db.session.commit()

        delete_calculation_id = calculation.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        calculation = self.calculation_repository.find_by_id(delete_calculation_id)

        result = self.app.get('/calculation/delete/' + str(calculation.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/calculation' in result.headers['Location'])

        # 削除した計算式が存在しないことを確認
        calculation = self.calculation_repository.find_by_id(delete_calculation_id)
        self.assertIsNone(calculation.id)

    # 存在しない計算式は削除できない
    def test_delete_calculation_fail(self):
        before = len(self.calculation_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/calculation/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/calculation' in result.headers['Location'])

        after = len(self.calculation_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

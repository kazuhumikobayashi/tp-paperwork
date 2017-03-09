from datetime import date, datetime

from nose.tools import ok_

from application import db
from application.domain.model.engineer_actual_result import EngineerActualResult
from application.domain.repository.engineer_actual_result_repository import EngineerActualResultRepository
from tests import BaseTestCase


class EngineerActualResultTests(BaseTestCase):

    def setUp(self):
        super(EngineerActualResultTests, self).setUp()
        self.engineer_actual_result_repository = EngineerActualResultRepository()

    def tearDown(self):
        super(EngineerActualResultTests, self).tearDown()

    # 技術者実績登録画面に遷移する。
    def test_get_engineer_actual_result_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer_actual_result/add?project_id=1')
        self.assertEqual(result.status_code, 200)

    # 技術者実績を保存する。
    def test_save_engineer_actual_result(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/engineer_actual_result/detail/1', data={
            'project_id': '1',
            'result_month': date.today(),
            'seq_no': 1,
            'engineer_id': 1,
            'fixed_flg': 1,
            'working_hours': 1,
            'adjustment_hours': 1,
            'billing_amount': 1,
            'billing_adjustment_amount': 1,
            'payment_amount': 1,
            'payment_adjustment_amount': 1,
            'carfare': 1,
            'remarks': 'remarks',
        })
        self.assertEqual(result.status_code, 302)

    # 技術者実績登録に失敗する。
    def test_save_engineer_actual_result_fail(self):
        before = len(self.engineer_actual_result_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 存在しないengineer_actual_result_idでは登録できない
        result = self.app.post('/engineer_actual_result/detail/99', data={
            'project_id': '1',
            'result_month': date.today(),
            'seq_no': 1,
            'engineer_id': 1,
            'fixed_flg': '1',
            'working_hours': 1,
            'adjustment_hours': 1,
            'billing_amount': 1,
            'billing_adjustment_amount': 1,
            'payment_amount': 1,
            'payment_adjustment_amount': 1,
            'carfare': 1,
            'remarks': 'remarks',
        })
        self.assertEqual(result.status_code, 404)

        after = len(self.engineer_actual_result_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 技術者実績を削除できる
    def test_delete_engineer_actual_result(self):
        # 削除用の技術者実績を登録
        engineer_actual_result = EngineerActualResult(
            project_id=1,
            result_month=date.today().strftime('%Y/%m/%d'),
            seq_no=1,
            engineer_id=1,
            fixed_flg='1',
            working_hours=1,
            adjustment_hours=1,
            billing_amount=1,
            billing_adjustment_amount=1,
            payment_amount=1,
            payment_adjustment_amount=1,
            carfare=1,
            remarks='remarks',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_actual_result)
        db.session.commit()

        delete_engineer_actual_result_id = engineer_actual_result.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        engineer_actual_result = self.engineer_actual_result_repository.find_by_id(delete_engineer_actual_result_id)

        result = self.app.get('/engineer_actual_result/delete/' + str(engineer_actual_result.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/detail/' + str(engineer_actual_result.project_id) in result.headers['Location'])

        # 削除した技術者実績が存在しないことを確認
        engineer_actual_result = self.engineer_actual_result_repository.find_by_id(delete_engineer_actual_result_id)
        self.assertIsNone(engineer_actual_result.id)

    # 存在しない技術者実績は削除できない
    def test_delete_engineer_actual_result_fail(self):
        before = len(self.engineer_actual_result_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer_actual_result/delete/0')
        # 削除できないことを確認
        self.assertEqual(result.status_code, 404)

        after = len(self.engineer_actual_result_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

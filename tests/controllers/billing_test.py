from datetime import datetime, date

from nose.tools import ok_

from application.domain.model.project_billing import ProjectBilling
from tests import BaseTestCase

from application import db
from application.domain.repository.project_billing_repository import ProjectBillingRepository


class BillingTest(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(BillingTest, cls).setUpClass()

    def setUp(self):
        super(BillingTest, self).setUp()
        self.billing_repository = ProjectBillingRepository()

    def tearDown(self):
        super(BillingTest, self).tearDown()

    # 請求詳細画面に遷移する。
    def test_get_billing(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        billing = self.billing_repository.find_all()[0]

        result = self.app.get('/billing/' + str(billing.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない請求の場合はnot_found
    def test_get_billing_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/billing/0')
        self.assertEqual(result.status_code, 404)

    # 請求情報を保存できる
    def test_save_company(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        billing = self.billing_repository.find_all()[0]

        expected = '単体テスト_変更'
        billing_id = billing.id

        result = self.app.post('/billing/' + str(billing_id), data={
            'billing_content': expected,
            'billing_amount': billing.billing_amount,
            'billing_confirmation_money': billing.billing_confirmation_money,
            'billing_transportation': billing.billing_transportation
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/billing/' + str(billing.id) in result.headers['Location'])

        billing = self.billing_repository.find_by_id(billing_id)
        actual = billing.billing_content
        self.assertEqual(actual, expected)

    # 請求情報を削除できる
    def test_delete_billing(self):
        # 削除用の請求情報を登録
        billing = ProjectBilling(
            project_detail_id=1,
            billing_month=date(2017, 1, 1).strftime('%Y/%m/%d'),
            billing_amount='1人月',
            billing_content='削除用請求',
            billing_confirmation_money=1000,
            billing_transportation=100,
            remarks='テスト',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(billing)
        db.session.commit()

        delete_billing_id = billing.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        billing = self.billing_repository.find_by_id(delete_billing_id)

        result = self.app.get('/billing/delete/' + str(billing.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project_billing/detail/' in result.headers['Location'])

        # 削除した請求が存在しないことを確認
        billing = self.billing_repository.find_by_id(delete_billing_id)
        self.assertIsNone(billing.id)

    # 存在しない会社は削除できない
    def test_delete_billing_fail(self):
        before = len(self.billing_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/billing/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/' in result.headers['Location'])

        after = len(self.billing_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

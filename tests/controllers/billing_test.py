from datetime import date, datetime

from nose.tools import ok_

from application import db
from application.domain.model.billing import Billing
from application.domain.repository.billing_repository import BillingRepository
from tests import BaseTestCase


class BillingTests(BaseTestCase):

    def setUp(self):
        super(BillingTests, self).setUp()
        self.billing_repository = BillingRepository()

    def tearDown(self):
        super(BillingTests, self).tearDown()

    # 請求登録画面に遷移する。
    def test_get_billing_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/billing/add?project_id=1')
        self.assertEqual(result.status_code, 200)

    # 請求を保存する。
    def test_save_billing(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/billing/detail/1', data={
            'project_id': '1',
            'engineer_id': '1',
            'sales_unit_price': '10',
            'payment_unit_price': '10',
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/31',
        })
        self.assertEqual(result.status_code, 302)

    # 請求登録に失敗する。
    def test_save_billing_fail(self):
        before = len(self.billing_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 存在しないbilling_idでは登録できない
        result = self.app.post('/billing/detail/99', data={
            'project_id': '1',
            'billing_month': date.today().strftime('%Y/%m/%d'),
            'billing_amount': 1,
            'billing_adjustment_amount': 1,
            'tax': 1,
            'carfare': 1,
            'scheduled_billing_date': date.today().strftime('%Y/%m/%d'),
            'billing_date': date.today().strftime('%Y/%m/%d'),
            'bill_output_date': date.today().strftime('%Y/%m/%d'),
            'scheduled_payment_date': date.today().strftime('%Y/%m/%d'),
            'payment_date': date.today().strftime('%Y/%m/%d'),
            'status': 1,
            'remarks': 'remarks'
        })
        self.assertEqual(result.status_code, 404)

        after = len(self.billing_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 請求を削除できる
    def test_delete_billing(self):
        # 削除用の請求を登録
        billing = Billing(
            project_id=1,
            billing_month=date.today().strftime('%Y/%m/%d'),
            billing_amount=1,
            billing_adjustment_amount=1,
            tax=1,
            carfare=1,
            scheduled_billing_date=date.today().strftime('%Y/%m/%d'),
            billing_date=date.today().strftime('%Y/%m/%d'),
            bill_output_date=date.today().strftime('%Y/%m/%d'),
            scheduled_payment_date=date.today().strftime('%Y/%m/%d'),
            payment_date=date.today().strftime('%Y/%m/%d'),
            status=1,
            remarks='remarks',
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
        ok_('/project/detail/' + str(billing.project_id) in result.headers['Location'])

        # 削除した請求が存在しないことを確認
        billing = self.billing_repository.find_by_id(delete_billing_id)
        self.assertIsNone(billing.id)

    # 存在しない請求は削除できない
    def test_delete_billing_fail(self):
        before = len(self.billing_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/billing/delete/0')
        # 削除できないことを確認
        self.assertEqual(result.status_code, 404)

        after = len(self.billing_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

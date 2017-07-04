from datetime import datetime, date

from nose.tools import ok_

from application import db
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.project_billing import ProjectBilling
from application.domain.model.project_month import ProjectMonth
from application.domain.repository.billing_sequence_repository import BillingSequenceRepository
from application.domain.repository.project_billing_repository import ProjectBillingRepository
from application.domain.repository.project_month_repository import ProjectMonthRepository
from tests import BaseTestCase


class ProjectBillingTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectBillingTests, cls).setUpClass()

    def setUp(self):
        super(ProjectBillingTests, self).setUp()
        self.project_billing_repository = ProjectBillingRepository()
        self.project_month_repository = ProjectMonthRepository()
        self.billing_sequence_repository = BillingSequenceRepository()

    def tearDown(self):
        super(ProjectBillingTests, self).tearDown()

    # 請求タブに遷移する。
    def test_get_project_billing(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_billing = self.project_month_repository.find_all()[0]

        result = self.app.get('/project/billing/' + str(project_billing.project.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないプロジェクトの場合はnot_found
    def test_get_project_billing_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/billing/0')
        self.assertEqual(result.status_code, 404)

    # 請求詳細画面に遷移する。
    def test_get_project_billing_month(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_billing = self.project_month_repository.find_all()[0]

        result = self.app.get('/project/billing/month/' + str(project_billing.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないプロジェクト年月の場合はnot_found
    def test_get_project_billing_month_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/billing/month/0')
        self.assertEqual(result.status_code, 404)

    # 請求詳細画面を保存できる
    def test_save_project_billing_month(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_month = self.project_month_repository.find_all()[0]

        expected = '単体テスト_変更'
        project_billing_id = project_month.id

        result = self.app.post('/project/billing/month/' + str(project_billing_id), data={
            'client_billing_no': expected,
            'billing_confirmation_money': project_month.billing_confirmation_money,
            'billing_transportation': project_month.billing_transportation,
            'deposit_date': project_month.deposit_date.strftime('%Y/%m/%d'),
            'remarks': project_month.remarks
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/billing/month/' + str(project_month.id) in result.headers['Location'])

        project_month = self.project_month_repository.find_by_id(project_billing_id)
        actual = project_month.client_billing_no
        self.assertEqual(actual, expected)

    # 存在しない請求の場合はnot_found
    def test_get_billing_project_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/billing/detail/0')
        self.assertEqual(result.status_code, 404)

    # 請求情報を保存できる
    def test_save_project_billing_detail(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        billing = self.project_billing_repository.find_all()[0]

        expected = '単体テスト_変更'
        billing_id = billing.id

        result = self.app.post('/project/billing/detail/' + str(billing_id), data={
            'billing_content': expected,
            'billing_amount': billing.billing_amount,
            'billing_confirmation_money': billing.billing_confirmation_money,
            'billing_transportation': billing.billing_transportation
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/billing/detail/' + str(billing.id) in result.headers['Location'])

        billing = self.project_billing_repository.find_by_id(billing_id)
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
        billing = self.project_billing_repository.find_by_id(delete_billing_id)

        result = self.app.get('/project/billing/delete/' + str(billing.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/billing/month/' in result.headers['Location'])

        # 削除した請求が存在しないことを確認
        billing = self.project_billing_repository.find_by_id(delete_billing_id)
        self.assertIsNone(billing.id)

    # 存在しない会社は削除できない
    def test_delete_billing_fail(self):
        before = len(self.project_billing_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/billing/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/' in result.headers['Location'])

        after = len(self.project_billing_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 請求詳細画面に遷移する。
    def test_get_detail_billing(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        billing = self.project_billing_repository.find_all()[0]

        result = self.app.get('/project/billing/detail/' + str(billing.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない請求の場合はnot_found
    def project_billing_repository(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/billing/0')
        self.assertEqual(result.status_code, 404)

    # 。請求済みフラグが更新されることを確認する
    def test_save_flag(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project_month_id = 5
        project_month = self.project_month_repository.find_by_id(project_month_id)

        # 請求入力済みフラグをチェック有りで更新する。
        excepted = InputFlag.done.value

        headers = [('X-Requested-With', 'XMLHttpRequest')]
        result = self.app.post('/project/billing/save_flag',
                               headers=headers,
                               data={
                                    'month_id': project_month.id,
                                    'input_flag': excepted
                               })
        self.assertEqual(result.status_code, 200)

        # DBのbilling_input_flag値が1になっていることを確認。
        project_month = self.project_month_repository.find_by_id(5)
        actual_input_flag = project_month.billing_input_flag.value
        self.assertEqual(actual_input_flag, excepted)

    def test_save_flag_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # xhrではない場合
        result = self.app.post('/project/billing/save_flag', data={
                                    'month_id': '2',
                                    'input_flag': InputFlag.done.value
                               })
        self.assertEqual(result.status_code, 404)

    # client_billing_noが発番されることを確認。
    def test_create_client_billing_no(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_month = self.project_month_repository.find_all()[0]
        project_billing_id = project_month.id

        result = self.app.post('/project/billing/month/' + str(project_billing_id), data={
            'client_billing_no': '',
            'billing_confirmation_money': project_month.billing_confirmation_money,
            'billing_transportation': project_month.billing_transportation,
            'deposit_date': project_month.deposit_date.strftime('%Y/%m/%d'),
            'remarks': project_month.remarks
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/billing/month/' + str(project_month.id) in result.headers['Location'])

        project_month = self.project_month_repository.find_by_id(project_billing_id)
        actual = project_month.client_billing_no
        self.assertIsNotNone(actual)

    # 請求番号が重複しない
    def test_duplicate_client_billing_no(self):
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 2017年度のシーケンスを取得
        billing_sequence = self.billing_sequence_repository.find_by_fiscal_year(17)

        # 連番が一つ先の注文書番号を登録しておく。
        client_billing_no = 'B' + str(billing_sequence.fiscal_year)\
                            + '-'\
                            + '{0:03d}'.format(billing_sequence.sequence + 1)

        project_month = ProjectMonth(
                            project_id=1,
                            project_month='2016/10/1',
                            billing_input_flag=InputFlag.yet,
                            deposit_input_flag=InputFlag.yet,
                            deposit_date='2016/10/1',
                            billing_estimated_money=10000,
                            billing_confirmation_money=10000,
                            billing_transportation=100,
                            remarks='remarks',
                            client_billing_no=client_billing_no,
                            created_at=datetime.today(),
                            created_user='test',
                            updated_at=datetime.today(),
                            updated_user='test')
        db.session.add(project_month)
        db.session.commit()

        # 新規作成時に発番が期待される注文書番号
        expected = 'B' + str(billing_sequence.fiscal_year)\
                   + '-'\
                   + '{0:03d}'.format(billing_sequence.sequence + 2)

        project_month = self.project_month_repository.find_all()[4]
        project_month.project_month = date(2016, 10, 1)
        db.session.add(project_month)
        db.session.commit()

        result = self.app.post('/project/billing/month/' + str(project_month.id), data={
            'client_billing_no': '',
            'billing_confirmation_money': project_month.billing_confirmation_money,
            'billing_transportation': project_month.billing_transportation,
            'deposit_date': project_month.deposit_date.strftime('%Y/%m/%d'),
            'remarks': project_month.remarks
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/billing/month/' + str(project_month.id) in result.headers['Location'])

        # 更新後のデータを確認する。
        actual = project_month.client_billing_no

        self.assertEqual(actual, expected)

    # 同じ顧客請求Noは登録できない
    def test_not_register_duplicate_client_billing_no(self):
        duplicate_client_billing_no = 'duplicate_client_billing_no'
        project_month = ProjectMonth(
                            project_id=1,
                            project_month='2016/10/1',
                            billing_input_flag=InputFlag.yet,
                            deposit_input_flag=InputFlag.yet,
                            deposit_date='2016/10/1',
                            billing_estimated_money=10000,
                            billing_confirmation_money=10000,
                            billing_transportation=100,
                            remarks='remarks',
                            client_billing_no=duplicate_client_billing_no,
                            created_at=datetime.today(),
                            created_user='test',
                            updated_at=datetime.today(),
                            updated_user='test')
        db.session.add(project_month)
        db.session.commit()

        project_month = self.project_month_repository.find_all()[4]
        project_month.project_month = date(2016, 10, 1)
        db.session.add(project_month)
        db.session.commit()

        result = self.app.post('/project/billing/month/' + str(project_month.id), data={
            'client_billing_no': duplicate_client_billing_no,
            'billing_confirmation_money': project_month.billing_confirmation_money,
            'billing_transportation': project_month.billing_transportation,
            'deposit_date': project_month.deposit_date.strftime('%Y/%m/%d'),
            'remarks': project_month.remarks
        })
        # 保存できない事を確認
        self.assertEqual(result.status_code, 200)

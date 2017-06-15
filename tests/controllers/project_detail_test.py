from datetime import datetime, date
from nose.tools import ok_

from application import db
from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.engineer import Engineer
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.site import Site
from application.domain.model.immutables.status import Status
from application.domain.model.immutables.tax import Tax
from application.domain.model.project import Project
from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.project_detail_repository import ProjectDetailRepository
from application.domain.repository.project_repository import ProjectRepository
from tests import BaseTestCase


class ProjectDetailTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectDetailTests, cls).setUpClass()

    def setUp(self):
        super(ProjectDetailTests, self).setUp()
        self.project_repository = ProjectRepository()
        self.project_detail_repository = ProjectDetailRepository()

    def tearDown(self):
        super(ProjectDetailTests, self).tearDown()

    # プロジェクト明細画面に遷移する。
    def test_get_project_detail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project_detail = self.project_detail_repository.find_all()[0]

        result = self.app.get('/project_detail/' + str(project_detail.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないプロジェクト明細画面には遷移できない。
    def test_get_project_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project_detail/0')
        self.assertEqual(result.status_code, 404)

    # プロジェクト明細登録画面に遷移する。
    def test_get_project_detail_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        result = self.app.get('/project_detail/create?project_id=' + str(project.id))
        self.assertEqual(result.status_code, 200)

    # プロジェクト明細を作業で新規登録できることを確認。
    def test_create_project_detail_by_work(self):
        before = len(self.project_detail_repository.find_all())
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # プロジェクトが保存できることを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.work,
            'work_name': '作業',
            'billing_money': '100000',
            'engineer_id': '',
            'billing_fraction_calculation1': '',
            'billing_fraction_calculation2': ''
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project_detail/' in result.headers['Location'])

        # 件数が増えていることを確認。
        after = len(self.project_detail_repository.find_all())
        # 件数が1件増えていることを確認
        self.assertEqual(before+1, after)

    # プロジェクト明細を技術者で新規登録できることを確認。
    def test_create_project_detail_by_engineer(self):
        before = len(self.project_detail_repository.find_all())
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # setup
        project = Project(
                    status=Status.done,
                    recorded_department_id=1,
                    estimation_no='M0001',
                    project_name='validation_test',
                    end_user_company_id=4,
                    client_company_id=3, start_date='2016/1/1',
                    end_date='2016/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')
        db.session.add(project)
        db.session.commit()

        # プロジェクトが保存できることを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '2',
            'billing_money': '100000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': 100,
            'billing_top_base_hour': 200,
            'billing_free_base_hour': '1/100, 1/200',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '1000',
            'billing_fraction': '1000',
            'billing_fraction_calculation1': '1',
            'billing_fraction_calculation2': '1',
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project_detail/' in result.headers['Location'])

        # 件数が増えていることを確認。
        after = len(self.project_detail_repository.find_all())
        # 件数が1件増えていることを確認
        self.assertEqual(before+1, after)

        # teardown
        db.session.delete(project)
        db.session.commit()

    # プロジェクト明細を削除できる
    def test_delete_project_detail(self):
        # 削除用のプロジェクトを登録
        project_detail = ProjectDetail(
            project_id=1,
            detail_type=DetailType.work,
            work_name='delete_project_detail_test',
            billing_money='100000',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project_detail)
        db.session.commit()

        delete_project_detail_id = project_detail.id
        project_id = project_detail.project.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        project_detail = self.project_detail_repository.find_by_id(delete_project_detail_id)

        result = self.app.get('/project_detail/delete/' + str(project_detail.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/contract/' + str(project_id) in result.headers['Location'])

        # 削除したプロジェクトが存在しないことを確認
        project_detail = self.project_detail_repository.find_by_id(delete_project_detail_id)
        self.assertIsNone(project_detail.id)

    # 存在しないプロジェクト明細は削除できない
    def test_delete_project_detail_fail(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project_detail/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project' in result.headers['Location'])

        after = len(self.project_detail_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    def test_required_work_name_if_work(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 作業名が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.work,
            'work_name': '',
            'billing_money': '100000',
            'engineer_id': '',
            'billing_fraction_calculation1': '',
            'billing_fraction_calculation2': ''
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_money_if_work(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求金額が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.work,
            'work_name': 'test_project_detail',
            'billing_money': '',
            'engineer_id': '',
            'billing_fraction_calculation1': '',
            'billing_fraction_calculation2': ''
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_engineer_id_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 技術者が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '',
            'billing_money': '100000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_money_id_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求金額が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_start_day_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求開始年月が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_end_day_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求終了年月が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_per_month_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求単価が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '',
            'billing_rule': Rule.fixed,
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_rule_if_engineer(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求単価が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': '',
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_bottom_base_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求フリー入力時間が空の場合、請求下限時間が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '',
            'billing_top_base_hour': '200',
            'billing_free_base_hour': '',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '1000',
            'billing_fraction': '1000',
            'billing_fraction_calculation1': '1',
            'billing_fraction_calculation2': '1',

        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_top_base_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求フリー入力時間が空の場合、請求上限時間が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '100',
            'billing_top_base_hour': '',
            'billing_free_base_hour': '',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '1000',
            'billing_fraction': '1000',
            'billing_fraction_calculation1': '1',
            'billing_fraction_calculation2': '1',

        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_free_base_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求下限・上限時間が空の場合、請求フリー入力時間が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '',
            'billing_top_base_hour': '',
            'billing_free_base_hour': '',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '1000',
            'billing_fraction': '1000',
            'billing_fraction_calculation1': '1',
            'billing_fraction_calculation2': '1',

        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_per_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求時間単価が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '100',
            'billing_top_base_hour': '200',
            'billing_free_base_hour': '1/100、1/200',
            'billing_per_hour': '',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '1000',
            'billing_fraction': '1000',
            'billing_fraction_calculation1': '1',
            'billing_fraction_calculation2': '1',

        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_per_bottom_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求△下限時間単価が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '100',
            'billing_top_base_hour': '200',
            'billing_free_base_hour': '1/100、1/200',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '',
            'billing_per_top_hour': '1000',
            'billing_fraction': '1000',
            'billing_fraction_calculation1': '1',
            'billing_fraction_calculation2': '1',

        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    def test_required_billing_per_top_hour_if_billing_rule_variable(self):
        before = len(self.project_detail_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_all()[0]

        # 請求＋上限時間単価が空だと明細を新規作成できないことを確認
        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': '1',
            'billing_money': '1000000',
            'billing_start_day': '2016/1',
            'billing_end_day': '2016/12',
            'billing_per_month': '100000',
            'billing_rule': Rule.variable,
            'billing_bottom_base_hour': '100',
            'billing_top_base_hour': '200',
            'billing_free_base_hour': '1/100、1/200',
            'billing_per_hour': '1000',
            'billing_per_bottom_hour': '1000',
            'billing_per_top_hour': '',
            'billing_fraction': '1000',
            'billing_fraction_calculation1': '1',
            'billing_fraction_calculation2': '1',

        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_detail_repository.find_all())
        self.assertEqual(before, after)

    # 支払い予定日を計算（支払いサイト30）
    def test_get_payment_date_by_site_30(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # set_up
        company = Company(
            company_name='会社',
            contract_date=datetime.today().strftime('%Y/%m/%d'),
            payment_site=Site.thirty,
            payment_tax=Tax.eight,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.bp,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='エンジニア',
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        project = Project(
            project_name='プロジェクト',
            status=Status.done,
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2017, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2017, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': engineer.id,
            'billing_money': '1000000',
            'billing_start_day': '2017/3',
            'billing_end_day': '2017/4',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
            'billing_fraction_calculation1': '',
            'billing_fraction_calculation2': ''
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project_detail/' in result.headers['Location'])

        # 契約期間は3月～4月で支払いサイトが30のため、
        # 3月のpayment_dateには翌月末日（2017/4/30（日））だが月末は前倒しのため、2017/4/28（金曜）、
        # 4月のpayment_dateには翌月末日（2017/5/31（水））が入る。
        expected_in_march = date(2017, 4, 28)
        expected_in_april = date(2017, 5, 31)

        # 保存したproject_detailを取得
        project_detail_id = result.headers['Location'].split('/')[-1]
        project_detail = self.project_detail_repository.find_by_id(project_detail_id)

        # 3月のpayment_dateには、2017/4/28が入っていることを確認。
        actual_in_march = project_detail.project_results[0].payment_expected_date
        self.assertEqual(actual_in_march, expected_in_march)

        # 4月のpayment_dateには、2017/5/31が入っていることを確認。
        actual_in_april = project_detail.project_results[1].payment_expected_date
        self.assertEqual(actual_in_april, expected_in_april)

    # 支払い予定日を計算（支払いサイト50）
    def test_get_payment_date_by_site_50(self):
        # ログイン
        self.app.post('/login', data={'shain_number': 'test1', 'password': 'test'})

        # set_up
        company = Company(
            company_name='会社',
            contract_date=datetime.today().strftime('%Y/%m/%d'),
            payment_site=Site.fifty,
            payment_tax=Tax.eight,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.bp,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='エンジニア',
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        project = Project(
            project_name='プロジェクト',
            status=Status.done,
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2017, 1, 1).strftime('%Y/%m/%d'),
            end_date=date(2017, 12, 31).strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': engineer.id,
            'billing_money': '1000000',
            'billing_start_day': '2017/3',
            'billing_end_day': '2017/4',
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed,
            'billing_fraction_calculation1': '',
            'billing_fraction_calculation2': ''
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project_detail/' in result.headers['Location'])

        # 契約期間は3月～4月で支払いサイトが50のため、
        # 3月のpayment_dateには翌月末日（2017/5/20（土））だが月末以外後ろ倒しのため、2017/4/22（月）、
        # 4月のpayment_dateには翌月末日（2017/6/20（火））が入る。
        expected_in_march = date(2017, 5, 22)
        expected_in_april = date(2017, 6, 20)

        # 保存したproject_detailを取得
        project_detail_id = result.headers['Location'].split('/')[-1]
        project_detail = self.project_detail_repository.find_by_id(project_detail_id)

        # 3月のpayment_dateには、2017/4/28が入っていることを確認。
        actual_in_march = project_detail.project_results[0].payment_expected_date
        self.assertEqual(actual_in_march, expected_in_march)

        # 4月のpayment_dateには、2017/5/31が入っていることを確認。
        actual_in_april = project_detail.project_results[1].payment_expected_date
        self.assertEqual(actual_in_april, expected_in_april)

    # ステータスが契約完了になった後でworkの明細を新規登録した場合、
    # プロジェクト開始～終了年月の請求レコードが作成される。
    def test_create_work_billing_when_status_done(self):
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # set_up
        project = self.project_repository.find_by_id(7)

        result = self.app.post('/contract/' + str(project.id), data={
            'status': Status.done.value,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': date(2017, 1, 1).strftime('%Y/%m/%d'),
            'end_date': date(2017, 3, 31).strftime('%Y/%m/%d'),
            'contract_form': project.contract_form.value,
            'billing_timing': project.billing_timing.value,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d')
        })
        self.assertEqual(result.status_code, 302)
        ok_('/contract' in result.headers['Location'])

        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.work.value,
            'work_name': 'test',
            'billing_money': '100000000',
            'engineer_id': '',
            'billing_fraction_calculation1': '',
            'billing_fraction_calculation2': ''
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project_detail/' in result.headers['Location'])
        project_detail_id = result.headers['Location'].split('/')[-1]

        project_detail = self.project_detail_repository.find_by_id(project_detail_id)
        # プロジェクト期間が2017年の1～3月のため、1～3月分の実績レコードが作成される。
        expected_1 = date(2017, 1, 1)
        expected_2 = date(2017, 2, 1)
        expected_3 = date(2017, 3, 1)
        actual_1 = project_detail.project_billings[0].billing_month
        actual_2 = project_detail.project_billings[1].billing_month
        actual_3 = project_detail.project_billings[2].billing_month

        self.assertEqual(actual_1, expected_1)
        self.assertEqual(actual_2, expected_2)
        self.assertEqual(actual_3, expected_3)

        # tear_down
        self.app.get('/project_detail/delete/' + str(project_detail.id))
        self.app.get('/project/delete/' + str(project.id))

from datetime import datetime, date
from decimal import Decimal

from nose.tools import ok_

from application import db
from application.domain.model.engineer import Engineer
from application.domain.model.engineer_history import EngineerHistory
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.status import Status
from application.domain.model.project import Project
from application.domain.repository.project_billing_repository import ProjectBillingRepository
from application.domain.repository.project_detail_repository import ProjectDetailRepository
from application.domain.repository.project_month_repository import ProjectMonthRepository
from application.domain.repository.project_repository import ProjectRepository
from tests import BaseTestCase

from application.domain.repository.project_result_repository import ProjectResultRepository


class ProjectResultTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectResultTests, cls).setUpClass()

    def setUp(self):
        super(ProjectResultTests, self).setUp()
        self.project_repository = ProjectRepository()
        self.project_result_repository = ProjectResultRepository()
        self.project_detail_repository = ProjectDetailRepository()
        self.project_billing_repository = ProjectBillingRepository()
        self.project_month_repository = ProjectMonthRepository()

    def tearDown(self):
        super(ProjectResultTests, self).tearDown()

    # 実績一覧に遷移する。
    def test_get_project_result(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_by_id(1)

        result = self.app.get('/project/result/' + str(project.id))
        self.assertEqual(result.status_code, 200)

    # 実績登録画面に遷移する。
    def test_get_result(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project_result = self.project_result_repository.find_all()[0]

        result = self.app.get('/project/result/detail/' + str(project_result.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない実績の場合はnot_found
    def test_get_result_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/result/detail/0')
        self.assertEqual(result.status_code, 404)

    # 実績を保存できる
    def test_save_result(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_result = self.project_result_repository.find_all()[0]

        expected = Decimal(300)
        project_result_id = project_result.id

        result = self.app.post('/project/result/detail/' + str(project_result_id), data={
            'work_time': expected
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/result/detail/' + str(project_result.id) in result.headers['Location'])

        project_result = self.project_result_repository.find_by_id(project_result_id)
        actual = project_result.work_time
        self.assertEqual(actual, expected)

    # 明細がengineerの場合、実績を更新すると同月の請求情報が新規作成される。
    def test_create_engineer_billing_when_update_result(self):
        before = len(self.project_billing_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # set_up
        project = Project(
            project_name='test_copy_project',
            project_name_for_bp='copy_project',
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='M0001-11',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2017, 1, 1),
            end_date=date(2017, 12, 31),
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            scope='test',
            contents=None,
            working_place=None,
            delivery_place=None,
            deliverables=None,
            inspection_date=None,
            responsible_person=None,
            quality_control=None,
            subcontractor=None,
            remarks=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        engineer = Engineer(
            engineer_name='エンジニア',
            company_id=5,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        history = EngineerHistory(
            engineer_id=engineer.id,
            payment_start_day=date(2016, 1, 1),
            payment_end_day=date(2099, 12, 31),
            payment_per_month=600000,
            payment_rule=Rule.fixed,
            payment_site=engineer.company.payment_site,
            payment_tax=engineer.company.payment_tax,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(history)
        db.session.commit()

        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': engineer.id,
            'billing_money': '100000000',
            'billing_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'billing_end_day': date(2017, 3, 1).strftime('%Y/%m'),
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed.value,
            'billing_fraction_rule': '',
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract/detail/' in result.headers['Location'])
        project_detail_id = result.headers['Location'].split('/')[-1]

        result = self.app.post('/project/contract/' + str(project.id), data={
            'status': Status.done.value,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': str(project.end_user_company_id),
            'client_company_id': str(project.client_company_id),
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form.value,
            'billing_timing': project.billing_timing.value
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract' in result.headers['Location'])

        project_detail = self.project_detail_repository.find_by_id(project_detail_id)
        project_result_id = project_detail.project_results[0].id

        # 実績を保存する。
        result = self.app.post('/project/result/detail/' + str(project_result_id), data={
            'work_time': '160.0',
            'billing_confirmation_money': '1000'
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/result/detail/' + str(project_result_id) in result.headers['Location'])

        # 請求のレコードが増えていることを確認する。
        after1 = len(self.project_billing_repository.find_all())
        self.assertEqual(before + 1, after1)

        # もう一度実績を保存すると既存の請求情報が更新されるため、請求のレコードが増えないことを確認する。
        result = self.app.post('/project/result/detail/' + str(project_result_id), data={
            'work_time': '160.0',
            'billing_confirmation_money': '1000'
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/result/detail/' + str(project_result_id) in result.headers['Location'])

        # 請求のレコード数が増えていないことを確認。
        after2 = len(self.project_billing_repository.find_all())
        self.assertEqual(after1, after2)

    # 請求確定金額がブランクの場合、請求情報が作成されるない
    def test_do_not_create_billing_when_billing_confirmation_money_none(self):
        before = len(self.project_billing_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # set_up
        project = Project(
            project_name='テスト',
            project_name_for_bp='テスト',
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='do_not_create_bill',
            end_user_company_id=4,
            client_company_id=3,
            start_date=date(2017, 1, 1),
            end_date=date(2017, 12, 31),
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            scope='test',
            contents=None,
            working_place=None,
            delivery_place=None,
            deliverables=None,
            inspection_date=None,
            responsible_person=None,
            quality_control=None,
            subcontractor=None,
            remarks=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        engineer = Engineer(
            engineer_name='エンジニア',
            company_id=5,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        history = EngineerHistory(
            engineer_id=engineer.id,
            payment_start_day=date(2016, 1, 1),
            payment_end_day=date(2099, 12, 31),
            payment_per_month=600000,
            payment_rule=Rule.fixed,
            payment_site=engineer.company.payment_site,
            payment_tax=engineer.company.payment_tax,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(history)
        db.session.commit()

        result = self.app.post('/project/contract/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': engineer.id,
            'billing_money': '100000000',
            'billing_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'billing_end_day': date(2017, 3, 1).strftime('%Y/%m'),
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed.value,
            'billing_fraction_rule': '',
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract/detail/' in result.headers['Location'])
        project_detail_id = result.headers['Location'].split('/')[-1]

        result = self.app.post('/project/contract/' + str(project.id), data={
            'status': Status.done.value,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': str(project.end_user_company_id),
            'client_company_id': str(project.client_company_id),
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form.value,
            'billing_timing': project.billing_timing.value
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/contract' in result.headers['Location'])

        project_detail = self.project_detail_repository.find_by_id(project_detail_id)
        project_result_id = project_detail.project_results[0].id

        # 実績を保存する。
        result = self.app.post('/project/result/detail/' + str(project_result_id), data={
            'work_time': '160.0',
            'billing_confirmation_money': ''
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project/result/detail/' + str(project_result_id) in result.headers['Location'])

        # 請求のレコード数が増えていないことを確認。
        after = len(self.project_billing_repository.find_all())
        self.assertEqual(before, after)

    # validationチェックに引っかかって実績を保存できない。
    def test_save_result_validation_error(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        project_result = self.project_result_repository.find_all()[0]

        project_result_id = project_result.id

        result = self.app.post('/project/result/detail/' + str(project_result_id), data={
            'work_time': 'aaa',
            'payment_transportation': 10000000000,
            'payment_adjustments': -10000000000
        })
        # 保存できないことを確認
        self.assertEqual(result.status_code, 200)

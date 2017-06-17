from datetime import date, datetime
from decimal import Decimal
from nose.tools import ok_

from application import db
from application.domain.model.engineer import Engineer
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.status import Status
from application.domain.model.project import Project
from application.domain.repository.project_billing_repository import ProjectBillingRepository
from application.domain.repository.project_detail_repository import ProjectDetailRepository
from application import db
from application.domain.model.project_billing import ProjectBilling
from tests import BaseTestCase

from application.domain.repository.project_result_repository import ProjectResultRepository


class ResultTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ResultTests, cls).setUpClass()

    def setUp(self):
        super(ResultTests, self).setUp()
        self.project_result_repository = ProjectResultRepository()
        self.project_detail_repository = ProjectDetailRepository()
        self.project_billing_repository = ProjectBillingRepository()

    def tearDown(self):
        super(ResultTests, self).tearDown()

    # 実績登録画面に遷移する。
    def test_get_result(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project_result = self.project_result_repository.find_all()[0]

        result = self.app.get('/result/' + str(project_result.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない実績の場合はnot_found
    def test_get_result_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/result/0')
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

        result = self.app.post('/result/' + str(project_result_id), data={
            'work_time': expected
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/result/' + str(project_result.id) in result.headers['Location'])

        project_result = self.project_result_repository.find_by_id(project_result_id)
        actual = project_result.work_time
        self.assertEqual(actual, expected)

    # engineer_historyがない技術者を登録。
    def test_save_proper_engineer(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })

        # set_up
        project_result = self.project_result_repository.find_all()[2]
        project_billing = ProjectBilling(
            project_detail_id = project_result.project_detail_id,
            billing_month = project_result.result_month,
            created_at = datetime.today(),
            created_user = 'test',
            updated_at = datetime.today(),
            updated_user = 'test'

        )
        db.session.add(project_billing)
        db.session.commit()

        # engineer_historyがないことを確認。
        self.assertEqual(project_result.project_detail.engineer.engineer_histories, [])

        expected = Decimal(300)
        project_result_id = project_result.id

        result = self.app.post('/result/' + str(project_result_id), data={
            'work_time': expected
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/result/' + str(project_result.id) in result.headers['Location'])

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
            deposit_date='20/12/31',
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

        result = self.app.post('/project_detail/create?project_id=' + str(project.id), data={
            'detail_type': DetailType.engineer,
            'engineer_id': engineer.id,
            'billing_money': '100000000',
            'billing_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'billing_end_day': date(2017, 3, 1).strftime('%Y/%m'),
            'billing_per_month': '100000',
            'billing_rule': Rule.fixed.value,
            'billing_fraction_calculation1': '',
            'billing_fraction_calculation2': '',
        })
        self.assertEqual(result.status_code, 302)
        ok_('/project_detail/' in result.headers['Location'])
        project_detail_id = result.headers['Location'].split('/')[-1]

        result = self.app.post('/contract/' + str(project.id), data={
            'status': Status.done.value,
            'recorded_department_id': project.recorded_department_id,
            'estimation_no': project.estimation_no,
            'project_name': project.project_name,
            'end_user_company_id': str(project.end_user_company_id),
            'client_company_id': str(project.client_company_id),
            'start_date': project.start_date.strftime('%Y/%m/%d'),
            'end_date': project.end_date.strftime('%Y/%m/%d'),
            'contract_form': project.contract_form.value,
            'billing_timing': project.billing_timing.value,
            'deposit_date': project.deposit_date.strftime('%Y/%m/%d')
        })
        self.assertEqual(result.status_code, 302)
        ok_('/contract' in result.headers['Location'])

        project_detail = self.project_detail_repository.find_by_id(project_detail_id)
        project_result_id = project_detail.project_results[0].id

        # 実績を保存する。
        result = self.app.post('/result/' + str(project_result_id), data={
            'work_time': '160.0',
            'billing_confirmation_money': '1000'
        })
        self.assertEqual(result.status_code, 302)
        ok_('/result/' + str(project_result_id) in result.headers['Location'])

        # 請求のレコードが増えていることを確認する。
        after1 = len(self.project_billing_repository.find_all())
        self.assertEqual(before + 1, after1)

        # もう一度実績を保存すると既存の請求情報が更新されるため、請求のレコードが増えないことを確認する。
        result = self.app.post('/result/' + str(project_result_id), data={
            'work_time': '160.0',
            'billing_confirmation_money': '1000'
        })
        self.assertEqual(result.status_code, 302)
        ok_('/result/' + str(project_result_id) in result.headers['Location'])

        # 請求のレコード数が増えていないことを確認。
        after2 = len(self.project_billing_repository.find_all())
        self.assertEqual(after1, after2)
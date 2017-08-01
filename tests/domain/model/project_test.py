from datetime import date, datetime

from application import db
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.status import Status
from application.domain.model.immutables.tax import Tax
from application.domain.model.project import Project
from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.project_repository import ProjectRepository
from tests import BaseTestCase


class ProjectTests(BaseTestCase):

    def setUp(self):
        super(ProjectTests, self).setUp()
        self.project_repository = ProjectRepository()

    def tearDown(self):
        super(ProjectTests, self).tearDown()

    def test_has_not_project_results_true(self):
        # set_up
        project = Project(
                    project_name='test_project',
                    project_name_for_bp='project',
                    status=Status.start,
                    recorded_department_id=1,
                    sales_person='営業担当',
                    estimation_no='test_project',
                    end_user_company_id=1,
                    client_company_id=5,
                    start_date=date.today(),
                    end_date='2099/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    estimated_total_amount=1000000,
                    scope='test',
                    contents=None,
                    working_place=None,
                    delivery_place=None, deliverables=None,
                    inspection_date=None,
                    responsible_person=None,
                    quality_control=None, subcontractor=None,
                    remarks=None,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        project_detail = ProjectDetail(
                    detail_type=DetailType.work,
                    work_name='test_project_detail',
                    billing_money='100000',
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        project.project_details.append(project_detail)
        db.session.add(project)
        db.session.commit()

        # project_resultが紐づいていない
        expected = []
        self.assertEqual(project.project_details[0].project_results, expected)

        # project_resultが紐づいていなければTrue
        actual = project.has_not_project_results()
        self.assertTrue(actual)

        # tear_down
        db.session.delete(project)
        db.session.delete(project_detail)
        db.session.commit()

    def test_has_not_project_results_false(self):
        project = self.project_repository.find_by_id(1)

        # project_resultが紐づいている
        self.assertIsNotNone(project.project_details[0].project_results[0])

        # 1件でもproject_resultが紐づいているならFalse
        actual = project.has_not_project_results()
        self.assertFalse(actual)

    def test_has_not_project_billings_true(self):
        # set_up
        project = Project(
                    project_name='test_project',
                    project_name_for_bp='project',
                    status=Status.start,
                    recorded_department_id=1,
                    sales_person='営業担当',
                    estimation_no='test_project',
                    end_user_company_id=1,
                    client_company_id=5,
                    start_date=date.today(),
                    end_date='2099/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    estimated_total_amount=1000000,
                    scope='test',
                    contents=None,
                    working_place=None,
                    delivery_place=None, deliverables=None,
                    inspection_date=None,
                    responsible_person=None,
                    quality_control=None, subcontractor=None,
                    remarks=None,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        project_detail = ProjectDetail(
                    detail_type=DetailType.work,
                    work_name='test_project_detail',
                    billing_money='100000',
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        project.project_details.append(project_detail)
        db.session.add(project)
        db.session.commit()

        # project_billingが紐づいていない
        expected = []
        self.assertEqual(project.project_details[0].project_billings, expected)

        # project_billingが紐づいていなければTrue
        actual = project.has_not_project_billings()
        self.assertTrue(actual)

        # tear_down
        db.session.delete(project)
        db.session.delete(project_detail)
        db.session.commit()

    def test_has_not_project_billings_false(self):
        project = self.project_repository.find_by_id(1)

        # project_billingが紐づいている
        self.assertIsNotNone(project.project_details[0].project_billings[0])

        # 1件でもproject_ billingが紐づいているならFalse
        actual = project.has_not_project_billings()
        self.assertFalse(actual)

    def test_has_not_project_months_true(self):
        # set_up
        project = Project(
                    project_name='test_project',
                    project_name_for_bp='project',
                    status=Status.start,
                    recorded_department_id=1,
                    sales_person='営業担当',
                    estimation_no='test_project',
                    end_user_company_id=1,
                    client_company_id=5,
                    start_date=date.today(),
                    end_date='2099/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    estimated_total_amount=1000000,
                    scope='test',
                    contents=None,
                    working_place=None,
                    delivery_place=None, deliverables=None,
                    inspection_date=None,
                    responsible_person=None,
                    quality_control=None, subcontractor=None,
                    remarks=None,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')
        db.session.add(project)
        db.session.commit()

        # project_monthが紐づいていない
        expected = []
        self.assertEqual(project.project_months, expected)

        # project_monthが紐づいていなければTrue
        actual = project.has_not_project_months()
        self.assertTrue(actual)

        # tear_down
        db.session.delete(project)
        db.session.commit()

    def test_has_not_project_months_false(self):
        project = self.project_repository.find_by_id(1)

        # project_monthが紐づいている
        self.assertIsNotNone(project.project_months[0])

        # 1件でもproject_monthが紐づいているならFalse
        actual = project.has_not_project_months()
        self.assertFalse(actual)

    def test_has_payment_true(self):
        project = self.project_repository.find_by_id(1)

        # project_detailが紐づいている
        self.assertIsNotNone(project.project_details[0])

        # bp所属ならTrue
        actual = project.has_payment()
        self.assertTrue(actual)

    def test_has_payment_false(self):
        # set_up
        project = Project(
                    project_name='test_project',
                    project_name_for_bp='project',
                    status=Status.start,
                    recorded_department_id=1,
                    sales_person='営業担当',
                    estimation_no='test_project',
                    end_user_company_id=1,
                    client_company_id=5,
                    start_date=date.today(),
                    end_date='2099/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    estimated_total_amount=1000000,
                    scope='test',
                    contents=None,
                    working_place=None,
                    delivery_place=None, deliverables=None,
                    inspection_date=None,
                    responsible_person=None,
                    quality_control=None, subcontractor=None,
                    remarks=None,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        project_detail = ProjectDetail(
                    detail_type=DetailType.work,
                    work_name='test_project_detail',
                    billing_money='100000',
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        project.project_details.append(project_detail)
        db.session.add(project)
        db.session.commit()

        # 作業だけならFalse
        actual = project.has_payment()
        self.assertFalse(actual)

    def test_tax_of_estimated_total_amount(self):
        project = Project(
                    project_name='test_project',
                    project_name_for_bp='project',
                    status=Status.start,
                    recorded_department_id=1,
                    sales_person='営業担当',
                    estimation_no='M2000',
                    end_user_company_id=1,
                    client_company_id=1,
                    start_date=date.today(),
                    end_date='2099/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    estimated_total_amount=1000000,
                    scope='test',
                    contents=None,
                    working_place=None,
                    delivery_place=None, deliverables=None,
                    inspection_date=None,
                    responsible_person=None,
                    quality_control=None, subcontractor=None,
                    remarks=None,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        # 消費税率が0のとき、消費税は0円となる。
        expected = 0
        project.billing_tax = Tax.zero
        actual = project.tax_of_estimated_total_amount()
        self.assertEqual(expected, actual)

        # estimated_total_amountが1000000なので、消費税率が8%のときは消費税が80000円となる。
        expected = 80000
        project.billing_tax = Tax.eight
        actual = project.tax_of_estimated_total_amount()
        self.assertEqual(expected, actual)

        # estimated_total_amountが1000000なので、消費税率が10%のときは消費税が100000円となる。
        expected = 100000
        project.billing_tax = Tax.ten
        actual = project.tax_of_estimated_total_amount()
        self.assertEqual(expected, actual)

    # 顧客会社を登録していない状態で、消費税計算を行った場合
    def test_tax_of_estimated_total_amount_fail(self):
        # set_up
        project = Project(
                    project_name='test_project',
                    project_name_for_bp='project',
                    status=Status.start,
                    recorded_department_id=1,
                    sales_person='営業担当',
                    estimation_no='M2000',
                    end_user_company_id=1,
                    client_company_id=None,
                    start_date=date.today(),
                    end_date='2099/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    estimated_total_amount=1000000,
                    scope='test',
                    contents=None,
                    working_place=None,
                    delivery_place=None, deliverables=None,
                    inspection_date=None,
                    responsible_person=None,
                    quality_control=None, subcontractor=None,
                    remarks=None,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        # 消費税は必ず0になる。
        expected = 0
        actual = project.tax_of_estimated_total_amount()
        self.assertEqual(expected, actual)

    def test_require_result_true(self):
        # set_up
        project = Project(
                    project_name='test_project',
                    project_name_for_bp='project',
                    status=Status.start,
                    recorded_department_id=1,
                    sales_person='営業担当',
                    estimation_no='test_require_result_true',
                    end_user_company_id=1,
                    client_company_id=5,
                    start_date=date.today(),
                    end_date='2099/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    estimated_total_amount=1000000,
                    scope='test',
                    contents=None,
                    working_place=None,
                    delivery_place=None, deliverables=None,
                    inspection_date=None,
                    responsible_person=None,
                    quality_control=None, subcontractor=None,
                    remarks=None,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        project_details = [
            ProjectDetail(
                project_id=project.id,
                detail_type=DetailType.engineer,
                engineer_id=1,
                billing_money=1,
                remarks=1,
                billing_start_day=project.start_date,
                billing_end_day=project.end_date,
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test'),
            ProjectDetail(
                project_id=project.id,
                detail_type=DetailType.engineer,
                engineer_id=2,
                billing_money=1,
                remarks=1,
                billing_start_day=project.start_date,
                billing_end_day=project.end_date,
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
        ]
        project.project_details = project_details

        db.session.add(project)
        db.session.commit()

        # 技術者だけならTrue
        actual = project.require_result()
        self.assertTrue(actual)

    def test_require_result_false(self):
        # set_up
        project = Project(
                    project_name='test_project',
                    project_name_for_bp='project',
                    status=Status.start,
                    recorded_department_id=1,
                    sales_person='営業担当',
                    estimation_no='test_require_result_false',
                    end_user_company_id=1,
                    client_company_id=5,
                    start_date=date.today(),
                    end_date='2099/12/31',
                    contract_form=Contract.blanket,
                    billing_timing=BillingTiming.billing_at_last,
                    estimated_total_amount=1000000,
                    scope='test',
                    contents=None,
                    working_place=None,
                    delivery_place=None, deliverables=None,
                    inspection_date=None,
                    responsible_person=None,
                    quality_control=None, subcontractor=None,
                    remarks=None,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        project_detail = ProjectDetail(
                    detail_type=DetailType.work,
                    work_name='test_project_detail',
                    billing_money='100000',
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')

        project.project_details.append(project_detail)
        db.session.add(project)
        db.session.commit()

        # 作業だけならFalse
        actual = project.require_result()
        self.assertFalse(actual)

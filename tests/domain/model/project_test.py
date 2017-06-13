from datetime import date, datetime

from application import db
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.status import Status
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
                    deposit_date='2099/12/31',
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
                    deposit_date='2099/12/31',
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
                    deposit_date='2099/12/31',
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

        # 1件でもproject_ monthが紐づいているならFalse
        actual = project.has_not_project_months()
        self.assertFalse(actual)

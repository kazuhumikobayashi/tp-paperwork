from datetime import date, timedelta

from application.domain.model.form.project_payment_form import ProjectPaymentForm
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.project_result import ProjectResult
from application.domain.repository.project_result_repository import ProjectResultRepository
from tests import BaseTestCase


class ProjectPaymentFormTests(BaseTestCase):
    def setUp(self):
        super(ProjectPaymentFormTests, self).setUp()
        self.project_result_repository = ProjectResultRepository()

    def tearDown(self):
        super(ProjectPaymentFormTests, self).tearDown()

    def test_has_project_results(self):
        project_payment_form = ProjectPaymentForm(
            project_id=1,
            project_month_id=1,
            month=date(2017, 1, 1))

        self.assertFalse(project_payment_form.has_project_results())

        self.project_result_repository.get_project_results(project_payment_form)
        self.assertTrue(project_payment_form.has_project_results())

    def test_has_not_project_results(self):
        project_payment_form = ProjectPaymentForm(
            project_id=1,
            project_month_id=1,
            month=date(2017, 1, 1))

        self.assertTrue(project_payment_form.has_not_project_results())

        self.project_result_repository.get_project_results(project_payment_form)
        self.assertFalse(project_payment_form.has_not_project_results())

    def test_is_closed(self):
        project_result_form = ProjectPaymentForm(project_id=1,
                                                 project_month_id=1,
                                                 month=date(2017, 1, 1))
        project_result_form.project_results = \
            [
                ProjectResult(payment_expected_date=None),
                ProjectResult(payment_flag=InputFlag.done, payment_expected_date=date.today() + timedelta(days=1))
            ]
        self.assertFalse(project_result_form.is_closed())

        project_result_form.project_results = \
            [
                ProjectResult(payment_flag=InputFlag.done, payment_expected_date=date.today() + timedelta(days=-1)),
                ProjectResult(payment_flag=InputFlag.done, payment_expected_date=date.today() + timedelta(days=-2)),
                ProjectResult(payment_flag=InputFlag.done, payment_expected_date=date.today() + timedelta(days=-3))
            ]
        self.assertTrue(project_result_form.is_closed())

    def test___repr__(self):
        project_payment_form = ProjectPaymentForm(
                                    project_id=1,
                                    project_month_id=1,
                                    month=date(2017, 1, 1))

        expected = "<ProjectPaymentForm:" + \
                   "'project_id='{}".format(project_payment_form.project_id) + \
                   "', project_month_id='{}".format(project_payment_form.project_month_id) + \
                   "', month='{}".format(project_payment_form.month) + \
                   "', project_results='{}".format(project_payment_form.project_results) + \
                   "'>"

        actual = str(project_payment_form)
        self.assertEqual(actual, expected)

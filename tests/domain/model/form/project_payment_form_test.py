from datetime import date

from application.domain.model.form.project_payment_form import ProjectPaymentForm
from tests import BaseTestCase


class ProjectPaymentFormTests(BaseTestCase):
    def setUp(self):
        super(ProjectPaymentFormTests, self).setUp()

    def tearDown(self):
        super(ProjectPaymentFormTests, self).tearDown()

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

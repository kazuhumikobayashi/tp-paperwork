from datetime import date

from application.domain.model.form.project_result_form import ProjectResultForm
from application.domain.model.immutables.input_flag import InputFlag
from tests import BaseTestCase


class ProjectResultFormTests(BaseTestCase):
    def setUp(self):
        super(ProjectResultFormTests, self).setUp()

    def tearDown(self):
        super(ProjectResultFormTests, self).tearDown()

    def test___repr__(self):
        project_result_form = ProjectResultForm(project_id=1,
                                                project_month_id=1,
                                                month=date(2017, 1, 1))

        expected = "<ProjectResultForm:" + \
                   "'project_id='{}".format(project_result_form.project_id) + \
                   "', project_month_id='{}".format(project_result_form.project_month_id) + \
                   "', month='{}".format(project_result_form.month) + \
                   "', project_results='{}".format(project_result_form.project_results) + \
                   "'>"

        actual = str(project_result_form)
        self.assertEqual(actual, expected)

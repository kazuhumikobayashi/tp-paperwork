from datetime import date

from application.domain.model.report.payment_list_by_department import PaymentListByDepartment
from application.domain.repository.department_repository import DepartmentRepository
from application.domain.repository.project_result_repository import ProjectResultRepository
from tests import BaseTestCase


class PaymentListByDepartmentTests(BaseTestCase):
    def setUp(self):
        super(PaymentListByDepartmentTests, self).setUp()
        self.department_repository = DepartmentRepository()
        self.project_result_repository = ProjectResultRepository()

    def tearDown(self):
        super(PaymentListByDepartmentTests, self).tearDown()

    def test___repr__(self):
        payment_list = PaymentListByDepartment(
                                department=self.department_repository.find_all()[0],
                                month=date(2017, 1, 1),
                                project_results=self.project_result_repository.find_all())

        expected = "<PaymentListByDepartment:"\
                   + "'department_name='{}".format(payment_list.department.department_name)\
                   + "', month='{}".format(payment_list.month)\
                   + "', project_results='{}".format(payment_list.project_results)\
                   + "'>"

        actual = str(payment_list)
        self.assertEqual(actual, expected)

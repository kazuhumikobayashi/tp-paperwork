
class PaymentListByDepartment(object):

    def __init__(self, department=None, month=None, project_results=None):
        self.department = department
        self.month = month
        self.project_results = project_results

    def __repr__(self):
        return "<PaymentListByDepartment:" + \
                "'department_name='{}".format(self.department.department_name) + \
                "', month='{}".format(self.month) + \
                "', project_results='{}".format(self.project_results) + \
                "'>"

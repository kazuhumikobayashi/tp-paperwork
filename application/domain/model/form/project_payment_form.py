from datetime import date

from application.domain.model.immutables.input_flag import InputFlag


class ProjectPaymentForm(object):

    def __init__(self, project_id=None, project_month_id=None, month=None):
        self.project_id = project_id
        self.project_month_id = project_month_id
        self.month = month
        self.project_results = None

    def has_project_results(self):
        return not self.has_not_project_results()

    def has_not_project_results(self):
        return not self.project_results

    def is_opened(self):
        return not self.is_closed()

    def is_closed(self):
        for result in self.project_results:
            if result.payment_expected_date:
                if result.payment_flag == InputFlag.yet or date.today() <= result.payment_expected_date:
                    return False
            else:
                return False
        return True

    def __repr__(self):
        return "<ProjectPaymentForm:" + \
                "'project_id='{}".format(self.project_id) + \
                "', project_month_id='{}".format(self.project_month_id) + \
                "', month='{}".format(self.month) + \
                "', project_results='{}".format(self.project_results) + \
                "'>"

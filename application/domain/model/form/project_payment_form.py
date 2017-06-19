from datetime import date


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
        return date.today().replace(day=1) <= self.month

    def is_closed(self):
        return not self.is_opened()

    def __repr__(self):
        return "<ProjectPaymentForm:" + \
                "'project_id='{}".format(self.project_id) + \
                "', project_month_id='{}".format(self.project_month_id) + \
                "', month='{}".format(self.month) + \
                "', project_results='{}".format(self.project_results) + \
                "'>"

class ProjectPaymentForm(object):

    def __init__(self, project_id=None, project_month_id=None, month=None):
        self.project_id = project_id
        self.project_month_id = project_month_id
        self.month = month
        self.project_results = None

    def __repr__(self):
        return "<ProjectPaymentForm:" + \
                "'project_id='{}".format(self.project_id) + \
                "', project_month_id='{}".format(self.project_month_id) + \
                "', month='{}".format(self.month) + \
                "', project_results='{}".format(self.project_results) + \
                "'>"

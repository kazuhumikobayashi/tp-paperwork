from datetime import date


class ProjectResultForm(object):

    def __init__(self, project_id=None, project_month_id=None, month=None):
        self.project_id = project_id
        self.project_month_id = project_month_id
        self.month = month
        self.project_results = None

    def is_opened(self):
        return self.month <= date.today().replace(day=1) and \
               False in [(r.work_time or 0) > 0 for r in self.project_results]

    def is_closed(self):
        return not self.is_opened()

    def __repr__(self):
        return "<ProjectResultForm:" + \
                "'project_id='{}".format(self.project_id) + \
                "', project_month_id='{}".format(self.project_month_id) + \
                "', month='{}".format(self.month) + \
                "', project_results='{}".format(self.project_results) + \
                "'>"

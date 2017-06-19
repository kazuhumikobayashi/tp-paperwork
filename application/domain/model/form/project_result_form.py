from datetime import date

from application.domain.model.immutables.input_flag import InputFlag


class ProjectResultForm(object):

    def __init__(self, project_id=None, project_month_id=None, month=None, input_flag=InputFlag.yet):
        self.project_id = project_id
        self.project_month_id = project_month_id
        self.month = month
        self.input_flag = input_flag
        self.project_results = None

    def is_opened(self):
        return self.input_flag == InputFlag.yet and self.month <= date.today().replace(day=1)

    def is_closed(self):
        return not self.is_opened()

    def __repr__(self):
        return "<ProjectResultForm:" + \
                "'project_id='{}".format(self.project_id) + \
                "', project_month_id='{}".format(self.project_month_id) + \
                "', month='{}".format(self.month) + \
                "', input_flag='{}".format(self.input_flag) + \
                "', project_results='{}".format(self.project_results) + \
                "'>"

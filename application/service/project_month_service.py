from application.domain.repository.project_month_repository import ProjectMonthRepository


class ProjectMonthService(object):
    repository = ProjectMonthRepository()

    def find_incomplete_results(self):
        return self.repository.find_incomplete_results()

    def find_incomplete_billings(self):
        return self.repository.find_incomplete_billings()

    def find_incomplete_deposits(self):
        return self.repository.find_incomplete_deposits()

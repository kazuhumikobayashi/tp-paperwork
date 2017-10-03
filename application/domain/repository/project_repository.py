from application.domain.model.immutables.status import Status

from sqlalchemy import asc

from application.domain.model.project import Project
from application.domain.repository.base_repository import BaseRepository


class ProjectRepository(BaseRepository):

    model = Project

    def find(self, page, project_name, estimation_no, status, end_user_company_id,
             client_company_id, recorded_department_id, start_date, end_date):
        query = self.model.query
        if project_name:
            query = query.filter(self.model.project_name.like('%' + project_name + '%'))
        if estimation_no:
            query = query.filter(self.model.estimation_no.like('%' + estimation_no + '%'))
        if status:
            query = query.filter(self.model.status.in_([Status.parse(st) for st in status]))         
        if end_user_company_id:
            query = query.filter(self.model.end_user_company_id.in_(end_user_company_id))
        if client_company_id:
            query = query.filter(self.model.client_company_id.in_(client_company_id))
        if recorded_department_id:
            query = query.filter(self.model.recorded_department_id.in_(recorded_department_id))
        if start_date:
            query = query.filter(self.model.start_date >= start_date)
        if end_date:
            query = query.filter(self.model.end_date <= end_date)
        pagination = \
            query.order_by('companies_1.company_name asc', 'companies_2.company_name asc',
                           'departments_1.department_name asc', self.model.project_name.asc(),
                           self.model.estimation_no.asc())\
            .paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_estimation_no(self, estimation_no):
        return self.model.query.filter(self.model.estimation_no == estimation_no).first()

    def find_incomplete_estimates(self):
        query = self.model.query.filter(self.model.status <= Status.received)
        query = query.order_by(asc(self.model.start_date), asc(self.model.project_name))
        return query.all()

    def save(self, project):
        if project.status == Status.done and project.has_not_project_results() and project.has_not_project_billings()\
                and project.has_not_project_months():
            project.create_project_months()

            for project_detail in project.project_details:
                if project_detail.is_engineer():
                    project_detail.create_results()
                else:
                    project_detail.create_billings()

        super(ProjectRepository, self).save(project)

    def create(self):
        return Project()

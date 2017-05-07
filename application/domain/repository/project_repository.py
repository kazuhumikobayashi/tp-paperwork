from application.domain.model.project import Project
from application.domain.repository.base_repository import BaseRepository


class ProjectRepository(BaseRepository):

    model = Project

    def find(self, page, start_date, end_date, project_name, end_user_company_id, client_company_id, recorded_department_id):
        query = self.model.query
        if start_date:
            query = query.filter(self.model.start_date >= start_date)
        if end_date:
            query = query.filter(self.model.end_date <= end_date)
        if project_name:
            query = query.filter(self.model.project_name.like('%' + project_name + '%'))
        if end_user_company_id:
            query = query.filter(self.model.end_user_company_id.in_(end_user_company_id))
        if client_company_id:
            query = query.filter(self.model.client_company_id.in_(client_company_id))
        if recorded_department_id:
            query = query.filter(self.model.recorded_department_id.in_(recorded_department_id))
        pagination = query.paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_estimation_no(self, estimation_no):
        return self.model.query.filter(self.model.estimation_no == estimation_no).first()

    def create(self):
        return Project()

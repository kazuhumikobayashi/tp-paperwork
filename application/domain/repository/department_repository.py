from application.domain.model.department import Department
from application.domain.repository.base_repository import BaseRepository


class DepartmentRepository(BaseRepository):

    model = Department

    def find(self, page, department_name):
        query = self.model.query
        if department_name:
            query = query.filter(self.model.department_name.like('%' + department_name + '%'))
        pagination = query.paginate(page, self.model.PER_PAGE)
        return pagination

    def create(self):
        return Department()

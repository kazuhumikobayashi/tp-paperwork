from application.domain.model.department import Department
from application.domain.repository.base_repository import BaseRepository


class DepartmentRepository(BaseRepository):

    model = Department

    def find(self, page, group_name, department_name):
        query = self.model.query
        if group_name:
            query = query.filter(self.model.group_name.like('%' + group_name + '%'))
        if department_name:
            query = query.filter(self.model.department_name.like('%' + department_name + '%'))
        pagination = query.order_by(self.model.created_at.asc()).paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_department_name(self, department_name):
        return self.model.query.filter(self.model.department_name == department_name).first()

    def create(self):
        return Department()

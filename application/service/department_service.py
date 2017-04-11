from application.domain.repository.department_repository import DepartmentRepository


class DepartmentService(object):
    repository = DepartmentRepository()

    def find(self, page, department_name):
        return self.repository.find(page, department_name)

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_all_for_select(self):
        ret = [('', '')]
        department_list = self.find_all_for_multi_select()
        ret.extend(department_list)
        return ret

    def find_all_for_multi_select(self):
        department_list = [(str(h.id), h.department_name) for h in self.find_all()]
        return department_list

    def find_by_id(self, department_id):
        return self.repository.find_by_id(department_id)

    def save(self, department):
        return self.repository.save(department)

    def destroy(self, department):
        return self.repository.destroy(department)

from application.domain.repository.engineer_actual_result_repository import EngineerActualResultRepository


class EngineerActualResultService(object):
    repository = EngineerActualResultRepository()

    def find(self, page, project_id, engineer_id):
        return self.repository.find(page, project_id, engineer_id)

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_by_id(self, assigned_member_id):
        return self.repository.find_by_id(assigned_member_id)

    def save(self, assigned_member):
        return self.repository.save(assigned_member)

    def destroy(self, assigned_member):
        return self.repository.destroy(assigned_member)

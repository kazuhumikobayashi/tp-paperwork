from application.domain.repository.project_detail_repository import ProjectDetailRepository


class ProjectDetailService(object):
    repository = ProjectDetailRepository()

    def find_by_id(self, project_detail_id):
        return self.repository.find_by_id(project_detail_id)

    def save(self, project_detail):
        return self.repository.save(project_detail)

    def destroy(self, project_detail):
        return self.repository.destroy(project_detail)

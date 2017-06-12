from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.base_repository import BaseRepository


class ProjectDetailRepository(BaseRepository):

    model = ProjectDetail

    def destroy(self, model):
        model.billing_money = None
        super(ProjectDetailRepository, self).destroy(model)

    def create(self):
        return ProjectDetail()

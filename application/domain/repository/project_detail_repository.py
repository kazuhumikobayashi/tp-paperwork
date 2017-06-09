from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.base_repository import BaseRepository


class ProjectDetailRepository(BaseRepository):

    model = ProjectDetail

    def create(self):
        return ProjectDetail()

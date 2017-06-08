from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.base_repository import BaseRepository


class ProjectDetailRepository(BaseRepository):

    model = ProjectDetail

    def find_incomplete_payments(self):
        return self.model.query\
                         .filter(self.model.detail_type == DetailType.engineer).all()

    def create(self):
        return ProjectDetail()

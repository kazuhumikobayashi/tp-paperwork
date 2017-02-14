from application.domain.model.project_attachment import ProjectAttachment
from application.domain.repository.base_repository import BaseRepository


class ProjectAttachmentRepository(BaseRepository):

    model = ProjectAttachment

    def create(self):
        return ProjectAttachment()

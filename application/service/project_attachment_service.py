from application.domain.repository.project_attachment_repository import ProjectAttachmentRepository


class ProjectAttachmentService(object):
    repository = ProjectAttachmentRepository()

    def find_by_id(self, project_attachment_id):
        return self.repository.find_by_id(project_attachment_id)

    def save(self, project_attachment):
        return self.repository.save(project_attachment)

    def destroy(self, project_attachment):
        return self.repository.destroy(project_attachment)

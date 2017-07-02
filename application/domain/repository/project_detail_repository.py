from application.domain.model.immutables.status import Status
from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.base_repository import BaseRepository


class ProjectDetailRepository(BaseRepository):

    model = ProjectDetail

    def find_by_bp_order_no(self, bp_order_no):
        return self.model.query.filter(self.model.bp_order_no == bp_order_no).first()

    def save(self, project_detail):
        if project_detail.project.status == Status.done\
                and not project_detail.project_results and not project_detail.project_billings:

            if project_detail.is_engineer():
                project_detail.create_results()
            else:
                project_detail.create_billings()
        super(ProjectDetailRepository, self).save(project_detail)

    def destroy(self, model):
        super(ProjectDetailRepository, self).destroy(model)

    def create(self):
        return ProjectDetail()

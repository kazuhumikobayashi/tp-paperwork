from application.domain.repository.project_result_repository import ProjectResultRepository
from tests import BaseTestCase


class ProjectResultRepositoryTests(BaseTestCase):

    def setUp(self):
        super(ProjectResultRepositoryTests, self).setUp()
        self.project_result_repository = ProjectResultRepository()

    def tearDown(self):
        super(ProjectResultRepositoryTests, self).tearDown()

    def test_create(self):
        project_result = self.project_result_repository.create()
        self.assertIsNone(project_result.id)

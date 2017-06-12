from application.domain.repository.project_repository import ProjectRepository
from tests import BaseTestCase

from application.domain.repository.project_result_repository import ProjectResultRepository

project_repository = ProjectRepository()


class ProjectResultTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectResultTests, cls).setUpClass()

    def setUp(self):
        super(ProjectResultTests, self).setUp()
        self.project_result_repository = ProjectResultRepository()

    def tearDown(self):
        super(ProjectResultTests, self).tearDown()

    # 実績一覧に遷移する。
    def test_get_project_result(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = project_repository.find_by_id(1)

        result = self.app.get('/project_result/' + str(project.id))
        self.assertEqual(result.status_code, 200)

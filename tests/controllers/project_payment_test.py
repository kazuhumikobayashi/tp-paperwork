from application.domain.repository.project_repository import ProjectRepository
from tests import BaseTestCase


class ProjectPaymentTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectPaymentTests, cls).setUpClass()

    def setUp(self):
        super(ProjectPaymentTests, self).setUp()
        self.project_repository = ProjectRepository()

    def tearDown(self):
        super(ProjectPaymentTests, self).tearDown()

    # 支払一覧に遷移する。
    def test_get_project_payment(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        project = self.project_repository.find_by_id(1)

        result = self.app.get('/project/payment/' + str(project.id))
        self.assertEqual(result.status_code, 200)

from io import BytesIO

from application.domain.repository.project_attachment_repository import ProjectAttachmentRepository
from tests import BaseTestCase


class AttachmentTests(BaseTestCase):

    def setUp(self):
        super(AttachmentTests, self).setUp()
        self.project_attachment_repository = ProjectAttachmentRepository()

    def tearDown(self):
        super(AttachmentTests, self).tearDown()

    # 添付文書がダウンロードできることを確認
    def test_download(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # download用の添付文書を登録
        file = (BytesIO(b'my file contents'), 'test_download.pdf')
        result = self.app.post('/project_attachment/create?project_id=1', data={
            'upload': file,
            'type': '1',
            'remarks': 'remarks'
        })
        self.assertEqual(result.status_code, 302)
        download_project_attachment_id = result.headers['Location'].split('/')[-1]
        project_attachment = self.project_attachment_repository.find_by_id(download_project_attachment_id)

        result = self.app.get('/attachment/download/' + str(project_attachment.attachment_id))
        self.assertEqual(result.status_code, 200)

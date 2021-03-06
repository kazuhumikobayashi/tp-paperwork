from datetime import datetime
from io import BytesIO

from nose.tools import ok_

from application import db
from application.domain.model.attachment import Attachment
from application.domain.model.immutables.project_attachment_type import ProjectAttachmentType
from application.domain.model.project_attachment import ProjectAttachment
from application.domain.repository.project_attachment_repository import ProjectAttachmentRepository
from tests import BaseTestCase


class ProjectAttachmentTests(BaseTestCase):

    def setUp(self):
        super(ProjectAttachmentTests, self).setUp()
        self.project_attachment_repository = ProjectAttachmentRepository()

    def tearDown(self):
        super(ProjectAttachmentTests, self).tearDown()

    # 添付文書登録画面に遷移する。
    def test_get_project_attachment_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/attachment/create?project_id=1')
        self.assertEqual(result.status_code, 200)

    # 添付文書を登録する。
    def test_create_project_attachment(self):
        before = len(self.project_attachment_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        file = (BytesIO(b'my file contents'), 'hello world.pdf')
        result = self.app.post('/project/attachment/create?project_id=1', data={
            'upload': file,
            'type': '1',
            'remarks': 'remarks'
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.project_attachment_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

    # 添付文書の登録に失敗する。
    def test_create_project_attachment_fail(self):
        before = len(self.project_attachment_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/project/attachment/create?project_id=1', data={
            'type': '1',
            'remarks': 'remarks'
        })
        self.assertEqual(result.status_code, 200)

        after = len(self.project_attachment_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 'png', 'jpg', 'jpeg', 'gif', 'pdf', 'xlsx', 'xls'以外は添付できない
    def test_create_project_attachment_extention_error(self):
        before = len(self.project_attachment_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        file = (BytesIO(b'my file contents'), 'hello world.exe')
        result = self.app.post('/project/attachment/create?project_id=1', data={
            'upload': file,
            'type': '1',
            'remarks': 'remarks'
        })
        self.assertEqual(result.status_code, 200)

        after = len(self.project_attachment_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 添付文書を編集する。
    def test_detail_project_attachment(self):
        expected = 'remarks_edit'
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/project/attachment/detail/1', data={
            'type': '1',
            'remarks': expected
        })
        self.assertEqual(result.status_code, 302)

        project_attachment = self.project_attachment_repository.find_by_id(1)
        actual = project_attachment.remarks
        self.assertEqual(actual, expected)

    # 添付文書編集に失敗する。
    def test_detail_project_attachment_fail(self):
        before = len(self.project_attachment_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 存在しないproject_attachment_idでは登録できない
        result = self.app.post('/project/attachment/detail/99', data={
            'type': '1',
            'remarks': 'remarks'
        })
        self.assertEqual(result.status_code, 404)

        after = len(self.project_attachment_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 添付文書を削除できる
    def test_delete_project_attachment(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 削除用の添付文書を登録
        file = (BytesIO(b'my file contents'), 'delete_project_attachment.pdf')
        result = self.app.post('/project/attachment/create?project_id=1', data={
            'upload': file,
            'type': '1',
            'remarks': 'remarks'
        })
        self.assertEqual(result.status_code, 302)
        delete_project_attachment_id = result.headers['Location'].split('/')[-1]
        project_attachment = self.project_attachment_repository.find_by_id(delete_project_attachment_id)

        result = self.app.get('/project/attachment/delete/' + str(project_attachment.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        print(result.headers['Location'])
        ok_('/contract/' + str(project_attachment.project_id) in result.headers['Location'])

        # 削除した添付文書が存在しないことを確認
        project_attachment = self.project_attachment_repository.find_by_id(delete_project_attachment_id)
        self.assertIsNone(project_attachment.id)

    # storageにファイルが存在しない場合でも削除できる
    def test_delete_project_attachment_not_exist_storage(self):
        delete_attachment = self.create_attachment()
        result = self.app.get('/project/attachment/delete/' + str(delete_attachment.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)

        # 削除した添付文書がDB上に存在しないことを確認
        project_attachment = self.project_attachment_repository.find_by_id(delete_attachment.id)
        self.assertIsNone(project_attachment.id)

    # 存在しない添付文書は削除できない
    def test_delete_project_attachment_fail(self):
        before = len(self.project_attachment_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/attachment/delete/0')
        # 削除できないことを確認
        self.assertEqual(result.status_code, 404)

        after = len(self.project_attachment_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # validationチェックに引っかかって添付文書を保存できない。
    def test_detail_project_attachment_validation_error(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/project/attachment/detail/1', data={
            'type': '',
            'remarks': ''
        })
        # 保存できないことを確認
        self.assertEqual(result.status_code, 200)

    def create_attachment(self):
        attachment = Attachment(
            filename='delete.pdf',
            storage_filename='#',
            size='10',
            content_type='pdf',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(attachment)
        db.session.commit()

        project_attachment = ProjectAttachment(
            project_id=1,
            attachment_id=attachment.id,
            type=ProjectAttachmentType.parse(1),
            remarks='remarks',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project_attachment)
        db.session.commit()
        return project_attachment

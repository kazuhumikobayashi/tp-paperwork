from datetime import datetime

from nose.tools import ok_

from application import db
from application.domain.model.attachment import Attachment
from application.domain.model.project_attachment import ProjectAttachment
from application.domain.repository.project_attachment_repository import ProjectAttachmentRepository
from tests import BaseTestCase


class ProjectAttachmentExceptStorageTests(BaseTestCase):

    def setUp(self):
        super(ProjectAttachmentExceptStorageTests, self).setUp()
        self.project_attachment_repository = ProjectAttachmentRepository()

    def tearDown(self):
        super(ProjectAttachmentExceptStorageTests, self).tearDown()

    # 添付文書登録画面に遷移する。
    def test_get_project_attachment_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project_attachment/create?project_id=1')
        self.assertEqual(result.status_code, 200)

    # 添付文書の登録に失敗する。
    def test_create_project_attachment_fail(self):
        before = len(self.project_attachment_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/project_attachment/create?project_id=1', data={
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

        result = self.app.post('/project_attachment/detail/1', data={
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
        result = self.app.post('/project_attachment/detail/99', data={
            'type': '1',
            'remarks': 'remarks'
        })
        self.assertEqual(result.status_code, 404)

        after = len(self.project_attachment_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 存在しない添付文書は削除できない
    def test_delete_project_attachment_fail(self):
        before = len(self.project_attachment_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project_attachment/delete/0')
        # 削除できないことを確認
        self.assertEqual(result.status_code, 404)

        after = len(self.project_attachment_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

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
            type=1,
            remarks='remarks',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project_attachment)
        db.session.commit()
        return project_attachment

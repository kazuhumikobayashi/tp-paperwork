import os
import shutil

from flask import session

from application import app
from application.domain.repository.excel import Excel
from application.domain.repository.user_repository import UserRepository
from tests import BaseTestCase


class ExcelTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ExcelTests, cls).setUpClass()
        shutil.copyfile('tests/fixture/test_template.xlsx', 'excel/templates/test_template.xlsx')

    @classmethod
    def tearDownClass(cls):
        super(ExcelTests, cls).tearDownClass()
        os.remove('excel/templates/test_template.xlsx')

    def setUp(self):
        super(ExcelTests, self).setUp()
        self.user_repository = UserRepository()
        with app.test_request_context():
            user = self.user_repository.find_by_id(1)
            session['user'] = user.serialize()
            excel = Excel("test_template.xlsx")
        self.excel = excel

    def tearDown(self):
        super(ExcelTests, self).tearDown()

    def test_new_load_template(self):
        expected = 'test_template.xlsx'
        self.assertEqual(self.excel.file_name, expected)

    def test_new(self):
        with app.test_request_context():
            user = self.user_repository.find_by_id(1)
            session['user'] = user.serialize()

            excel = Excel()
            # 新規作成時はファイル名がない
            self.assertIsNone(excel.file_name)

    def test_save(self):
        # ファイル名を指定しないで保存した場合はテンプレートを同じファイル名
        self.excel.save()
        expected = 'test_template.xlsx'
        self.assertEqual(self.excel.file_name, expected)

        # ファイル名を指定して保存した場合は指定したファイル名になる
        expected = 'test_save_rename.xlsx'
        self.excel.save(expected)
        self.assertEqual(self.excel.file_name, expected)

    def test_download(self):
        with app.test_request_context():
            # ダウンロードできることを確認
            self.excel.save()
            result = self.excel.download()
            self.assertEqual(result.status_code, 200)

    def test_active(self):
        expected = 'シート1'
        ws = self.excel.active
        self.assertEqual(ws.title, expected)

        # シート追加
        expected = 'シート2'
        self.excel.workbook.create_sheet(title=expected)
        self.excel.active = 1
        ws = self.excel.active
        self.assertEqual(ws.title, expected)

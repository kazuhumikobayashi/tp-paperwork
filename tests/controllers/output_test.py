from datetime import date, datetime

from application.domain.model.immutables.output_type import OutputType
from application.domain.model.project_result import ProjectResult
from application.domain.repository.project_detail_repository import ProjectDetailRepository
from tests import BaseTestCase


class OutputTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(OutputTests, cls).setUpClass()

    def setUp(self):
        super(OutputTests, self).setUp()
        self.project_detail_repository = ProjectDetailRepository()

    def tearDown(self):
        super(OutputTests, self).tearDown()

    # 帳票出力画面に遷移する。
    def test_get_output(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/output/')
        self.assertEqual(result.status_code, 200)

    # 支払一覧をダウンロードする。
    def test_download_payment_list(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # set_up
        # BPの支払情報を複数作成
        project_detail = self.project_detail_repository.find_by_id(2)
        for n in range(10):
            project_result = ProjectResult(
                                project_detail_id=2,
                                result_month='2016/8/1',
                                work_time=200,
                                payment_confirmation_money=100000,
                                remarks='remarks',
                                created_at=datetime.today(),
                                created_user='test',
                                updated_at=datetime.today(),
                                updated_user='test')
            project_detail.project_results.append(project_result)

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.payment_list.value,
            'month': date(2016, 8, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

    # 支払一覧の帳票をダウンロード。
    # output.pyの21行目がfalseの場合（他の帳票のテストが全て埋まればこのテストは不要になる予定）。
    def test_download_else_report_download(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.yayoi_interface.value,
            'month': date(2016, 8, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

    # 支払一覧をダウンロードする（engineer_historyがない場合）。
    def test_download_payment_list_without_engineer_history(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # set_up
        # 支払情報を複数作成
        project_detail = self.project_detail_repository.find_by_id(2)
        for n in range(10):
            project_result = ProjectResult(
                                project_detail_id=2,
                                result_month='2018/8/1',
                                work_time=200,
                                payment_confirmation_money=100000,
                                remarks='remarks',
                                created_at=datetime.today(),
                                created_user='test',
                                updated_at=datetime.today(),
                                updated_user='test')
            project_detail.project_results.append(project_result)

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.payment_list.value,
            'month': date(2018, 8, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

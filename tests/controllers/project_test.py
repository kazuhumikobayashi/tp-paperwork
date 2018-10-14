from urllib.parse import urlencode

from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from nose.tools import ok_

from application import db
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.status import Status
from application.domain.model.project import Project
from application.domain.model.project_detail import ProjectDetail
from application.domain.repository.estimation_sequence_repository import EstimationSequenceRepository
from application.domain.repository.project_repository import ProjectRepository
from tests import BaseTestCase


class ProjectTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectTests, cls).setUpClass()

    def setUp(self):
        super(ProjectTests, self).setUp()
        self.project_repository = ProjectRepository()
        self.estimation_sequence_repository = EstimationSequenceRepository()

    def tearDown(self):
        super(ProjectTests, self).tearDown()

    # プロジェクトの検索画面に遷移する。
    def test_get_project(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_project_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/page/2')
        self.assertEqual(result.status_code, 200)

    # プロジェクトを検索する。
    def test_search_project(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'project_name': 'test',
                                  'estimation_no': 'M17-17001',
                                  'status': '99',
                                  'end_user_company_id': '1',
                                  'client_company_id': '1',
                                  'recorded_department_id': '1', 
                                  'start_date': '2016/1/1',                                  
                                  'end_date': '2017/1/1'})
        result = self.app.get('/project/?' + query_string)

        self.assertEqual(result.status_code, 200)

    # プロジェクト登録画面に遷移する。
    def test_get_project_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/create')
        self.assertEqual(result.status_code, 200)

    # プロジェクトをコピーできる
    def test_copy_project(self):
        # コピー用のプロジェクトを登録
        project = Project(
            project_name='test_copy_project',
            project_name_for_bp='copy_project',
            status=Status.done,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='test_copy_project',
            end_user_company_id=1,
            client_company_id=5,
            start_date=date.today(),
            end_date='2099/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            scope='test',
            contents=None,
            working_place=None,
            delivery_place=None,
            deliverables=None,
            inspection_date=date.today(),
            responsible_person=None,
            quality_control=None,
            subcontractor=None,
            remarks=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')

        db.session.add(project)
        db.session.commit()

        original_project_id = project.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        original = self.project_repository.find_by_id(original_project_id)

        result = self.app.post('/project/copy/' + str(original.id), data={
            'project_name': 'test_copy_project_after',
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/31'
        })
        # コピーできることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/contract' in result.headers['Location'])

        copy_project_id = result.headers['Location'].split('/')[-1]

        # コピーしたプロジェクトが存在することを確認
        copy = self.project_repository.find_by_id(copy_project_id)
        self.assertIsNotNone(copy.id)

        # コピーしたプロジェクトのステータスが「01:契約開始」に戻っていることを確認
        self.assertEqual(copy.status, Status.start)

    # プロジェクトを削除できる
    def test_delete_project(self):
        # 削除用のプロジェクトを登録
        project = Project(
            project_name='test_delete_project',
            project_name_for_bp='delete_project',
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='test_delete_project',
            end_user_company_id=1,
            client_company_id=5,
            start_date=date.today(),
            end_date='2099/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            scope='test',
            contents=None,
            working_place=None,
            delivery_place=None,
            deliverables=None,
            inspection_date=None,
            responsible_person=None,
            quality_control=None,
            subcontractor=None,
            remarks=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        delete_project_id = project.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        project = self.project_repository.find_by_id(delete_project_id)

        result = self.app.get('/project/delete/' + str(project.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project' in result.headers['Location'])

        # 削除したプロジェクトが存在しないことを確認
        project = self.project_repository.find_by_id(delete_project_id)
        self.assertIsNone(project.id)

    # 存在しないプロジェクトは削除できない
    def test_delete_project_fail(self):
        before = len(self.project_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/project/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project' in result.headers['Location'])

        after = len(self.project_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # コピー時に見積番号が重複しない
    def test_duplicate_copy_project(self):
        # 今年度のシーケンスを取得
        year = int(date.today().strftime('%y'))
        if int(date.today().strftime('%m')) >= 10:
            year += 1

        estimation_sequence = self.estimation_sequence_repository.find_by_fiscal_year(year)
        print(estimation_sequence)
        # これから作成される見積番号を作成
        estimation_no = 'M' + str(estimation_sequence.fiscal_year)\
                        + '-'\
                        + str(estimation_sequence.fiscal_year)\
                        + '{0:03d}'.format(estimation_sequence.sequence + 1)

        # コピー時に発番が期待される見積番号
        expected = 'M' + str(estimation_sequence.fiscal_year)\
                   + '-'\
                   + str(estimation_sequence.fiscal_year)\
                   + '{0:03d}'.format(estimation_sequence.sequence + 2)

        # コピー用のプロジェクトを登録
        project = Project(
            project_name='test_copy_project',
            project_name_for_bp='copy_project',
            status=Status.done,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no=estimation_no,
            end_user_company_id=1,
            client_company_id=5,
            start_date=date.today(),
            end_date='2099/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            scope='test',
            contents=None,
            working_place=None,
            delivery_place=None,
            deliverables=None,
            inspection_date=None,
            responsible_person=None,
            quality_control=None,
            subcontractor=None,
            remarks=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')

        db.session.add(project)
        db.session.commit()

        original_project_id = project.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        original = self.project_repository.find_by_id(original_project_id)

        result = self.app.post('/project/copy/' + str(original.id), data={
            'project_name': 'test_copy_project_after',
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/31'
        })
        # コピーできることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/contract' in result.headers['Location'])

        copy_project_id = result.headers['Location'].split('/')[-1]

        # コピーしたプロジェクトが存在することを確認
        copy = self.project_repository.find_by_id(copy_project_id)
        self.assertIsNotNone(copy.id)

        # コピーしたプロジェクトの見積番号を確認
        self.assertEqual(copy.estimation_no, expected)

    # 開始日より終了日の方が小さい場合はエラー
    def test_start_date_less_than_end_date(self):
        before = len(self.project_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/project/create', data={
            'project_name': 'テスト',
            'start_date': date(2017, 4, 1).strftime('%Y/%m/%d'),
            'end_date': date(2017, 3, 31).strftime('%Y/%m/%d'),
        })
        self.assertEqual(result.status_code, 200)

        # 件数が変わっていないことを確認。
        after = len(self.project_repository.find_all())
        self.assertEqual(before, after)

    # プロジェクトをコピー時に開始日、終了日がプロジェクト明細にもコピーされる
    def test_copy_project_detail_start_date_and_end_date(self):
        # コピー用のプロジェクトを登録
        project = Project(
            project_name='test_copy_project',
            project_name_for_bp='copy_project',
            status=Status.done,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='test_copy_project_detail_start_date_and_end_date',
            end_user_company_id=1,
            client_company_id=5,
            start_date='2016/9/1',
            end_date='2016/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            scope='test',
            contents=None,
            working_place=None,
            delivery_place=None,
            deliverables=None,
            inspection_date=None,
            responsible_person=None,
            quality_control=None,
            subcontractor=None,
            remarks=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')

        project_details = [
            ProjectDetail(
                project_id=project.id,
                detail_type=DetailType.engineer,
                engineer_id=1,
                billing_money=1,
                remarks=1,
                billing_start_day=project.start_date,
                billing_end_day=project.end_date,
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test'),
            ProjectDetail(
                project_id=project.id,
                detail_type=DetailType.engineer,
                engineer_id=2,
                billing_money=1,
                remarks=1,
                billing_start_day=project.start_date,
                billing_end_day=project.end_date,
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
        ]
        project.project_details = project_details

        db.session.add(project)
        db.session.commit()

        original_project_id = project.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        original = self.project_repository.find_by_id(original_project_id)

        result = self.app.post('/project/copy/' + str(original.id), data={
            'project_name': 'test_copy_project_after',
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': (date.today() + relativedelta(months=1)).strftime('%Y/%m/%d')
        })
        # コピーできることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/contract' in result.headers['Location'])

        copy_project_id = result.headers['Location'].split('/')[-1]

        # コピーしたプロジェクトが存在することを確認
        copy = self.project_repository.find_by_id(copy_project_id)
        self.assertIsNotNone(copy.id)

        # コピーしたプロジェクト明細の契約開始日、終了日がプロジェクト開始日、終了日になっていることを確認
        for detail in copy.project_details:
            self.assertEqual(copy.start_date, detail.billing_start_day)
            self.assertEqual(copy.end_date, detail.billing_end_day)

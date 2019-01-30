from urllib.parse import urlencode

from datetime import datetime

from dateutil.relativedelta import relativedelta

from application import db
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.status import Status
from application.domain.model.project import Project
from application.domain.repository.project_month_repository import ProjectMonthRepository
from tests import BaseTestCase


class SearchResultTests(BaseTestCase):

    def setUp(self):
        super(SearchResultTests, self).setUp()
        self.project_month_repository = ProjectMonthRepository()

    def tearDown(self):
        super(SearchResultTests, self).tearDown()

    # 実績検索画面に遷移する。
    def test_get_result_search(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/search/result/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_result_search_page2(self):

        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        today = datetime.today().date()
        first_day = today.replace(day=1)
        last_first_day = first_day + relativedelta(months=-1)
        last_day = first_day + relativedelta(months=1, days=-1)
        # プロジェクトを新規作成
        project = Project(
            project_name='test_result_search_page2',
            end_user_company_id=4,
            client_company_id=3,
            start_date=last_first_day.strftime('%Y/%m/%d'),
            end_date=last_day.strftime('%Y/%m/%d'),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project)
        db.session.commit()

        project_id = project.id

        # 2ページ目に行くように12件明細情報を登録する
        for num in range(12):
            self.app.post('/project/contract/create?project_id=' + str(project_id), data={
                'detail_type': DetailType.engineer,
                'engineer_id': num+1,
                'billing_money': '100000000',
                'billing_start_day': last_first_day.strftime('%Y/%m'),
                'billing_end_day': last_day.strftime('%Y/%m'),
                'billing_per_month': '100000',
                'billing_rule': Rule.fixed.value,
                'billing_fraction_rule': '',
            })

        # 契約完了にして、実績データを作成する
        result = self.app.post('/project/contract/' + str(project_id), data={
            'status': Status.done.value,
            'recorded_department_id': '1',
            'estimation_no': 'M0024',
            'project_name': '日付テスト',
            'end_user_company_id': '4',
            'client_company_id': '3',
            'start_date': last_first_day.strftime('%Y/%m/%d'),
            'end_date': last_day.strftime('%Y/%m/%d'),
            'contract_form': Contract.blanket.value,
            'billing_timing': BillingTiming.billing_at_last.value
        })
        self.assertEqual(result.status_code, 302)

        result = self.app.get('/search/result/page/2')
        self.assertEqual(result.status_code, 200)

    # 実績を検索する。
    def test_search_result(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'project_name': 'test',
                                  'estimation_no': 'test',
                                  'result_input_flag': '1',
                                  'end_user_company_id': '1',
                                  'client_company_id': '1',
                                  'recorded_department_id': '1',
                                  'engineer_name': 'test',
                                  'result_month_from': '2016/1',
                                  'result_month_to': '2017/1'})
        result = self.app.get('/search/result/?' + query_string)

        self.assertEqual(result.status_code, 200)

    # 日付をブランク、実績未入力で実績を検索する
    def test_search_result_blank_day(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'project_name': 'test',
                                  'estimation_no': 'test',
                                  'result_input_flag': '0',
                                  'end_user_company_id': '1',
                                  'client_company_id': '1',
                                  'recorded_department_id': '1',
                                  'engineer_name': 'test',
                                  'result_month_from': '',
                                  'result_month_to': ''})
        result = self.app.get('/search/result/?' + query_string)

        self.assertEqual(result.status_code, 200)

    # 見積Noをカンマ区切りで検索し、２ページ目に遷移する。
    def test_search_billing_by_searching_in_comma(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'project_name': '',
                                  'estimation_no': 'M11,M12',
                                  'engineer_name': '',
                                  'result_month_from': '',
                                  'result_month_to': ''})
        result = self.app.get('/search/result/page/2?' + query_string)
        self.assertEqual(result.status_code, 200)

    # 見積Noを全角スペース区切りで検索し、２ページ目に遷移する。
    def test_search_billing_by_searching_in_space(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'project_name': '',
                                  'estimation_no': 'M11　M12',
                                  'engineer_name': '',
                                  'result_month_from': '',
                                  'result_month_to': ''})
        result = self.app.get('/search/result/page/2?' + query_string)
        self.assertEqual(result.status_code, 200)

    # 見積Noを半角スペース区切りで検索し、２ページ目に遷移する。
    def test_search_billing_by_searching_in_half_space(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        query_string = urlencode({'project_name': '',
                                  'estimation_no': 'M11 M12',
                                  'engineer_name': '',
                                  'result_month_from': '',
                                  'result_month_to': ''})
        result = self.app.get('/search/result/page/2?' + query_string)
        self.assertEqual(result.status_code, 200)

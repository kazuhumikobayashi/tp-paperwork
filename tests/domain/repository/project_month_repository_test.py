from application.domain.repository.project_month_repository import ProjectMonthRepository
from tests import BaseTestCase


class ProjectMonthRepositoryTests(BaseTestCase):

    def setUp(self):
        super(ProjectMonthRepositoryTests, self).setUp()
        self.project_month_repository = ProjectMonthRepository()

    def tearDown(self):
        super(ProjectMonthRepositoryTests, self).tearDown()

    def test_find_by_estimation_no_including_comma_in_billing_search(self):
        # 'M11-0001,M12-0001'で検索するとM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_month_repository.find_by_billing(page=1, project_name='',
                                                                   estimation_no='M11-0001,M12-0001',
                                                                   billing_input_flag='', deposit_input_flag='',
                                                                   end_user_company_id='', client_company_id='',
                                                                   recorded_department_id='',
                                                                   deposit_date_from='', deposit_date_to='')
        result = len([project_month for project_month in pagination.items])
        self.assertEquals(expect, result)

    def test_find_over_ten_by_estimation_no_including_comma_in_billing_search(self):
        # 'M11,M12-0001'で検索するとM11-0000〜M11-0009、M12-0001の計11件がヒットする
        expect = 11
        pagination_1 = self.project_month_repository.find_by_billing(page=1, project_name='',
                                                                     estimation_no='M11,M12-0001',
                                                                     billing_input_flag='', deposit_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='',
                                                                     deposit_date_from='', deposit_date_to='')
        result_1 = len([project_month for project_month in pagination_1.items])
        pagination_2 = self.project_month_repository.find_by_billing(page=2, project_name='',
                                                                     estimation_no='M11,M12-0001',
                                                                     billing_input_flag='', deposit_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='',
                                                                     deposit_date_from='', deposit_date_to='')
        result_2 = len([project_month for project_month in pagination_2.items])
        self.assertEquals(expect, result_1+result_2)

    def test_find_by_estimation_no_including_space_in_billing_search(self):
        # 'M11-0001　M12-0001'で検索するとM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_month_repository.find_by_billing(page=1, project_name='',
                                                                   estimation_no='M11-0001　M12-0001',
                                                                   billing_input_flag='', deposit_input_flag='',
                                                                   end_user_company_id='', client_company_id='',
                                                                   recorded_department_id='',
                                                                   deposit_date_from='', deposit_date_to='')
        result = len([project_month for project_month in pagination.items])
        self.assertEquals(expect, result)

    def test_find_over_ten_by_estimation_no_including_space_in_billing_search(self):
        # 'M11　M12-0001'で検索するとM11-0000〜M11-0009、M11-0001の計11件がヒットする
        expect = 11
        pagination_1 = self.project_month_repository.find_by_billing(page=1, project_name='',
                                                                     estimation_no='M11　M12-0001',
                                                                     billing_input_flag='', deposit_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='',
                                                                     deposit_date_from='', deposit_date_to='')
        result_1 = len([project_month for project_month in pagination_1.items])
        pagination_2 = self.project_month_repository.find_by_billing(page=2, project_name='',
                                                                     estimation_no='M11　M12-0001',
                                                                     billing_input_flag='', deposit_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='',
                                                                     deposit_date_from='', deposit_date_to='')
        result_2 = len([project_month for project_month in pagination_2.items])
        self.assertEquals(expect, result_1+result_2)

    def test_find_by_estimation_no_including_half_space_in_billing_search(self):
        # 'M11-0001 M12-0001'で検索するとM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_month_repository.find_by_billing(page=1, project_name='',
                                                                   estimation_no='M11-0001 M12-0001',
                                                                   billing_input_flag='', deposit_input_flag='',
                                                                   end_user_company_id='', client_company_id='',
                                                                   recorded_department_id='',
                                                                   deposit_date_from='', deposit_date_to='')
        result = len([project_month for project_month in pagination.items])
        self.assertEquals(expect, result)

    def test_find_over_ten_by_estimation_no_including_half_space_in_billing_search(self):
        # 'M11 M12-0001'で検索するとM11-0000〜M11-0009、M11-0001の計11件がヒットする
        expect = 11
        pagination_1 = self.project_month_repository.find_by_billing(page=1, project_name='',
                                                                     estimation_no='M11 M12-0001',
                                                                     billing_input_flag='', deposit_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='',
                                                                     deposit_date_from='', deposit_date_to='')
        result_1 = len([project_month for project_month in pagination_1.items])
        pagination_2 = self.project_month_repository.find_by_billing(page=2, project_name='',
                                                                     estimation_no='M11 M12-0001',
                                                                     billing_input_flag='', deposit_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='',
                                                                     deposit_date_from='', deposit_date_to='')
        result_2 = len([project_month for project_month in pagination_2.items])
        self.assertEquals(expect, result_1+result_2)

    def test_find_by_estimation_no_including_comma_or_space_in_front_and_behind_in_billing_search(self):
        # ' 　,M11-0001,M12-0001 ,　'（前後にスペースや,あり）で検索してもM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_month_repository.find_by_billing(page=1, project_name='',
                                                                   estimation_no=' 　,M11-0001,M12-0001 ,　',
                                                                   billing_input_flag='', deposit_input_flag='',
                                                                   end_user_company_id='', client_company_id='',
                                                                   recorded_department_id='',
                                                                   deposit_date_from='', deposit_date_to='')
        result = len([project_month for project_month in pagination.items])
        self.assertEquals(expect, result)

    def test_create(self):
        project_result = self.project_month_repository.create()
        self.assertIsNone(project_result.id)

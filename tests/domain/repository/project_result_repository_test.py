from application.domain.repository.project_result_repository import ProjectResultRepository
from tests import BaseTestCase


class ProjectResultRepositoryTests(BaseTestCase):

    def setUp(self):
        super(ProjectResultRepositoryTests, self).setUp()
        self.project_result_repository = ProjectResultRepository()

    def tearDown(self):
        super(ProjectResultRepositoryTests, self).tearDown()

    def test_find_by_estimation_no_including_comma_in_result_search(self):
        # 'M11-0001,M12-0001'で検索するとM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_result_repository.find_by_result(page=1, project_name='',
                                                                   estimation_no='M11-0001,M12-0001',
                                                                   result_input_flag='',
                                                                   end_user_company_id='', client_company_id='',
                                                                   recorded_department_id='', engineer_name='',
                                                                   result_month_from='', result_month_to='')
        result = len([project_result for project_result in pagination.items])
        self.assertEquals(expect, result)

    def test_find_over_ten_by_estimation_no_including_comma_in_result_search(self):
        # 'M11,M12-0001'で検索するとM11-0000〜M11-0009、M12-0001の計11件がヒットする
        expect = 11
        pagination_1 = self.project_result_repository.find_by_result(page=1, project_name='',
                                                                     estimation_no='M11,M12-0001',
                                                                     result_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='', engineer_name='',
                                                                     result_month_from='', result_month_to='')
        result_1 = len([project_result for project_result in pagination_1.items])
        pagination_2 = self.project_result_repository.find_by_result(page=2, project_name='',
                                                                     estimation_no='M11,M12-0001',
                                                                     result_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='', engineer_name='',
                                                                     result_month_from='', result_month_to='')
        result_2 = len([project_result for project_result in pagination_2.items])
        self.assertEquals(expect, result_1+result_2)

    def test_find_by_estimation_no_including_space_in_result_search(self):
        # 'M11-0001　M12-0001'で検索するとM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_result_repository.find_by_result(page=1, project_name='',
                                                                   estimation_no='M11-0001　M12-0001',
                                                                   result_input_flag='',
                                                                   end_user_company_id='', client_company_id='',
                                                                   recorded_department_id='', engineer_name='',
                                                                   result_month_from='', result_month_to='')
        result = len([project_result for project_result in pagination.items])
        self.assertEquals(expect, result)

    def test_find_over_ten_by_estimation_no_including_space_in_result_search(self):
        # 'M11　M12-0001'で検索するとM11-0000〜M11-0009、M11-0001の計11件がヒットする
        expect = 11
        pagination_1 = self.project_result_repository.find_by_result(page=1, project_name='',
                                                                     estimation_no='M11　M12-0001',
                                                                     result_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='', engineer_name='',
                                                                     result_month_from='', result_month_to='')
        result_1 = len([project_result for project_result in pagination_1.items])
        pagination_2 = self.project_result_repository.find_by_result(page=2, project_name='',
                                                                     estimation_no='M11　M12-0001',
                                                                     result_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='', engineer_name='',
                                                                     result_month_from='', result_month_to='')
        result_2 = len([project_result for project_result in pagination_2.items])
        self.assertEquals(expect, result_1+result_2)

    def test_find_by_estimation_no_including_half_space_in_result_search(self):
        # 'M11-0001 M12-0001'で検索するとM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_result_repository.find_by_result(page=1, project_name='',
                                                                   estimation_no='M11-0001 M12-0001',
                                                                   result_input_flag='',
                                                                   end_user_company_id='', client_company_id='',
                                                                   recorded_department_id='', engineer_name='',
                                                                   result_month_from='', result_month_to='')
        result = len([project_result for project_result in pagination.items])
        self.assertEquals(expect, result)

    def test_find_over_ten_by_estimation_no_including_half_space_in_result_search(self):
        # 'M11 M12-0001'で検索するとM11-0000〜M11-0009、M11-0001の計11件がヒットする
        expect = 11
        pagination_1 = self.project_result_repository.find_by_result(page=1, project_name='',
                                                                     estimation_no='M11 M12-0001',
                                                                     result_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='', engineer_name='',
                                                                     result_month_from='', result_month_to='')
        result_1 = len([project_result for project_result in pagination_1.items])
        pagination_2 = self.project_result_repository.find_by_result(page=2, project_name='',
                                                                     estimation_no='M11 M12-0001',
                                                                     result_input_flag='',
                                                                     end_user_company_id='', client_company_id='',
                                                                     recorded_department_id='', engineer_name='',
                                                                     result_month_from='', result_month_to='')
        result_2 = len([project_result for project_result in pagination_2.items])
        self.assertEquals(expect, result_1+result_2)

    def test_find_by_estimation_no_including_comma_or_space_in_front_and_behind_in_result_search(self):
        # ' 　,M11-0001,M12-0001 ,　'（前後にスペースや,あり）で検索してもM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_result_repository.find_by_result(page=1, project_name='',
                                                                   estimation_no=' 　,M11-0001,M12-0001 ,　',
                                                                   result_input_flag='',
                                                                   end_user_company_id='', client_company_id='',
                                                                   recorded_department_id='', engineer_name='',
                                                                   result_month_from='', result_month_to='')
        result = len([project_result for project_result in pagination.items])
        self.assertEquals(expect, result)

    def test_find_by_estimation_no_including_comma_in_payment_search(self):
        # 'M11-0001,M12-0001'で検索するとM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_result_repository.find_by_payment(page=1, project_name='',
                                                                    estimation_no='M11-0001,M12-0001',
                                                                    input_flag='',
                                                                    end_user_company_id='', client_company_id='',
                                                                    recorded_department_id='', engineer_name='',
                                                                    payment_expected_date_from='',
                                                                    payment_expected_date_to='')
        result = len([project_result for project_result in pagination.items])
        self.assertEquals(expect, result)

    def test_find_over_ten_by_estimation_no_including_comma_in_payment_search(self):
        # 'M11,M12-0001'で検索するとM11-0000〜M11-0009、M12-0001の計11件がヒットする
        expect = 11
        pagination_1 = self.project_result_repository.find_by_payment(page=1, project_name='',
                                                                      estimation_no='M11,M12-0001',
                                                                      input_flag='',
                                                                      end_user_company_id='', client_company_id='',
                                                                      recorded_department_id='', engineer_name='',
                                                                      payment_expected_date_from='',
                                                                      payment_expected_date_to='')
        result_1 = len([project_result for project_result in pagination_1.items])
        pagination_2 = self.project_result_repository.find_by_payment(page=2, project_name='',
                                                                      estimation_no='M11,M12-0001',
                                                                      input_flag='',
                                                                      end_user_company_id='', client_company_id='',
                                                                      recorded_department_id='', engineer_name='',
                                                                      payment_expected_date_from='',
                                                                      payment_expected_date_to='')
        result_2 = len([project_result for project_result in pagination_2.items])
        self.assertEquals(expect, result_1+result_2)

    def test_find_by_estimation_no_including_space_in_payment_search(self):
        # 'M11-0001　M12-0001'で検索するとM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_result_repository.find_by_payment(page=1, project_name='',
                                                                    estimation_no='M11-0001　M12-0001',
                                                                    input_flag='',
                                                                    end_user_company_id='', client_company_id='',
                                                                    recorded_department_id='', engineer_name='',
                                                                    payment_expected_date_from='',
                                                                    payment_expected_date_to='')
        result = len([project_result for project_result in pagination.items])
        self.assertEquals(expect, result)

    def test_find_over_ten_by_estimation_no_including_space_in_payment_search(self):
        # 'M11　M12-0001'で検索するとM11-0000〜M11-0009、M11-0001の計11件がヒットする
        expect = 11
        pagination_1 = self.project_result_repository.find_by_payment(page=1, project_name='',
                                                                      estimation_no='M11　M12-0001',
                                                                      input_flag='',
                                                                      end_user_company_id='', client_company_id='',
                                                                      recorded_department_id='', engineer_name='',
                                                                      payment_expected_date_from='',
                                                                      payment_expected_date_to='')
        result_1 = len([project_result for project_result in pagination_1.items])
        pagination_2 = self.project_result_repository.find_by_payment(page=2, project_name='',
                                                                      estimation_no='M11　M12-0001',
                                                                      input_flag='',
                                                                      end_user_company_id='', client_company_id='',
                                                                      recorded_department_id='', engineer_name='',
                                                                      payment_expected_date_from='',
                                                                      payment_expected_date_to='')
        result_2 = len([project_result for project_result in pagination_2.items])
        self.assertEquals(expect, result_1+result_2)

    def test_find_by_estimation_no_including_half_space_in_payment_search(self):
        # 'M11-0001 M12-0001'で検索するとM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_result_repository.find_by_payment(page=1, project_name='',
                                                                    estimation_no='M11-0001 M12-0001',
                                                                    input_flag='',
                                                                    end_user_company_id='', client_company_id='',
                                                                    recorded_department_id='', engineer_name='',
                                                                    payment_expected_date_from='',
                                                                    payment_expected_date_to='')
        result = len([project_result for project_result in pagination.items])
        self.assertEquals(expect, result)

    def test_find_over_ten_by_estimation_no_including_half_space_in_payment_search(self):
        # 'M11 M12-0001'で検索するとM11-0000〜M11-0009、M11-0001の計11件がヒットする
        expect = 11
        pagination_1 = self.project_result_repository.find_by_payment(page=1, project_name='',
                                                                      estimation_no='M11 M12-0001',
                                                                      input_flag='',
                                                                      end_user_company_id='', client_company_id='',
                                                                      recorded_department_id='', engineer_name='',
                                                                      payment_expected_date_from='',
                                                                      payment_expected_date_to='')
        result_1 = len([project_result for project_result in pagination_1.items])
        pagination_2 = self.project_result_repository.find_by_payment(page=2, project_name='',
                                                                      estimation_no='M11 M12-0001',
                                                                      input_flag='',
                                                                      end_user_company_id='', client_company_id='',
                                                                      recorded_department_id='', engineer_name='',
                                                                      payment_expected_date_from='',
                                                                      payment_expected_date_to='')
        result_2 = len([project_result for project_result in pagination_2.items])
        self.assertEquals(expect, result_1+result_2)

    def test_find_by_estimation_no_including_comma_or_space_in_front_and_behind_in_payment_search(self):
        # ' 　,M11-0001,M12-0001 ,　'（前後にスペースや,あり）で検索してもM11-0001とM12-0001の計2件がヒットする
        expect = 2
        pagination = self.project_result_repository.find_by_payment(page=1, project_name='',
                                                                    estimation_no=' 　,M11-0001,M12-0001 ,　',
                                                                    input_flag='',
                                                                    end_user_company_id='', client_company_id='',
                                                                    recorded_department_id='', engineer_name='',
                                                                    payment_expected_date_from='',
                                                                    payment_expected_date_to='')
        result = len([project_result for project_result in pagination.items])
        self.assertEquals(expect, result)

    def test_create(self):
        project_result = self.project_result_repository.create()
        self.assertIsNone(project_result.id)

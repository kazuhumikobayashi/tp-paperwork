from datetime import date, datetime

from application import db
from application.domain.model.company import Company
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.engineer import Engineer
from application.domain.model.engineer_business_category import EngineerBusinessCategory
from application.domain.model.engineer_history import EngineerHistory
from application.domain.model.engineer_skill import EngineerSkill
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.fraction import Fraction
from application.domain.model.immutables.gender import Gender
from application.domain.model.immutables.holiday_flag import HolidayFlag
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.immutables.output_type import OutputType
from application.domain.model.immutables.round import Round
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.site import Site
from application.domain.model.immutables.status import Status
from application.domain.model.immutables.tax import Tax
from application.domain.model.project import Project
from application.domain.model.project_detail import ProjectDetail
from application.domain.model.project_month import ProjectMonth
from application.domain.model.project_result import ProjectResult
from application.domain.repository.project_detail_repository import ProjectDetailRepository
from application.domain.repository.project_month_repository import ProjectMonthRepository
from tests import BaseTestCase


class OutputTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(OutputTests, cls).setUpClass()

    def setUp(self):
        super(OutputTests, self).setUp()
        self.project_detail_repository = ProjectDetailRepository()
        self.project_month_repository = ProjectMonthRepository()

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

    # 出力項目のデータが存在するケース
    def test_download_project_list_01(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # setup
        company = Company(
            company_name='プロジェクト一覧テスト01',
            company_name_kana='プロジェクトイチランテスト01',
            company_short_name="プロテス01",
            contract_date=date.today(),
            postal_code='000-0000',
            address='住所',
            phone='000-0000',
            fax='000-0000',
            client_code='0001',
            bp_code='9999',
            billing_site=Site.twenty_five,
            payment_site=Site.thirty,
            billing_tax=Tax.zero,
            payment_tax=Tax.eight,
            bank_id='2',
            bank_holiday_flag=HolidayFlag.before,
            remarks='備考',
            print_name='印刷用宛名',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.our_company,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='プロジェクト一覧テスト01',
            engineer_name_kana='プロジェクトイチランテスト01',
            birthday=date.today(),
            gender=Gender.male,
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        engineer_history = EngineerHistory(
            engineer_id=engineer.id,
            payment_start_day=date(2016, 1, 1),
            payment_end_day=date(2018, 12, 31),
            payment_per_month=100,
            payment_site=Site.twenty_five,
            payment_tax=Tax.eight,
            payment_rule=Rule.fixed,
            payment_bottom_base_hour=100,
            payment_top_base_hour=100,
            payment_free_base_hour='',
            payment_per_hour='1/100, 1/150',
            payment_per_bottom_hour=100,
            payment_per_top_hour=100,
            payment_fraction=Fraction.hundred,
            payment_fraction_rule=Round.down,
            payment_condition='test',
            remarks='test',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_history)

        engineer_business_category = EngineerBusinessCategory(
            engineer_id=engineer.id,
            business_category_id=3,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_business_category)

        for num in range(2):
            engineer_skill = EngineerSkill(
                engineer_id=engineer.id,
                skill_id=num + 1,
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
            db.session.add(engineer_skill)

        project = Project(
            project_name='プロジェクト一覧テスト01',
            project_name_for_bp='プロジェクト一覧テスト01',
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='プロジェクト一覧テスト01',
            end_user_company_id=company.id,
            client_company_id=company.id,
            start_date='2018/1/1',
            end_date='2018/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            billing_tax=Tax.zero,
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

        project_detail = ProjectDetail(
            project_id=project.id,
            detail_type=DetailType.engineer,
            work_name='プロジェクト一覧テスト01',
            engineer_id=engineer.id,
            billing_money=100,
            remarks='remarks',
            billing_start_day='2017/1/1',
            billing_end_day='2018/12/31',
            billing_per_month=100,
            billing_rule=Rule.fixed,
            billing_bottom_base_hour=120,
            billing_top_base_hour=200,
            billing_free_base_hour='billing_free_base_hour',
            billing_per_hour='billing_per_hour',
            billing_per_bottom_hour=120,
            billing_per_top_hour=200,
            billing_fraction=Fraction.one,
            billing_fraction_rule=Round.down,
            bp_order_no='bp_order_no',
            client_order_no_for_bp='client_order_no_for_bp',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test', )
        db.session.add(project_detail)
        db.session.commit()

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.project_list.value,
            'month': date(2018, 8, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

    # 出力項目のデータが存在しないケース
    def test_download_project_list_02(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # setup
        company = Company(
            company_name='プロジェクト一覧テスト02',
            company_name_kana=None,
            company_short_name=None,
            contract_date=None,
            postal_code=None,
            address=None,
            phone=None,
            fax=None,
            client_code=None,
            bp_code=None,
            billing_site=None,
            payment_site=None,
            billing_tax=None,
            payment_tax=None,
            bank_id=None,
            bank_holiday_flag=None,
            remarks=None,
            print_name=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.bp,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='プロジェクト一覧テスト02',
            engineer_name_kana=None,
            birthday=None,
            gender=Gender.male,
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        project = Project(
            project_name='プロジェクト一覧テスト02',
            project_name_for_bp=None,
            status=Status.start,
            recorded_department_id=None,
            sales_person=None,
            estimation_no=None,
            end_user_company_id=None,
            client_company_id=None,
            start_date='2018/1/1',
            end_date='2018/12/31',
            contract_form=None,
            billing_timing=None,
            estimated_total_amount=None,
            billing_tax=None,
            scope=None,
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

        project_detail = ProjectDetail(
            project_id=project.id,
            detail_type=DetailType.engineer,
            work_name=None,
            engineer_id=engineer.id,
            billing_money=None,
            remarks=None,
            billing_start_day='2018/1/1',
            billing_end_day='2018/12/31',
            billing_per_month=None,
            billing_rule=None,
            billing_bottom_base_hour=None,
            billing_top_base_hour=None,
            billing_free_base_hour=None,
            billing_per_hour=None,
            billing_per_bottom_hour=None,
            billing_per_top_hour=None,
            billing_fraction=None,
            billing_fraction_rule=None,
            bp_order_no=None,
            client_order_no_for_bp=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test', )
        db.session.add(project_detail)
        db.session.commit()

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.project_list.value,
            'month': date(2018, 8, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

    # 請求ルール・支払ルールが'変動'、かつ基準時間入力ありのテストケース
    def test_download_project_list_03(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # setup
        company = Company(
            company_name='プロジェクト一覧テスト03',
            company_name_kana='プロジェクトイチランテスト03',
            company_short_name="プロテス03",
            contract_date=date.today(),
            postal_code='000-0000',
            address='住所',
            phone='000-0000',
            fax='000-0000',
            client_code='0001',
            bp_code='9999',
            billing_site=Site.twenty_five,
            payment_site=Site.thirty,
            billing_tax=Tax.zero,
            payment_tax=Tax.eight,
            bank_id='2',
            bank_holiday_flag=HolidayFlag.before,
            remarks='備考',
            print_name='印刷用宛名',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.bp,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='プロジェクト一覧テスト03',
            engineer_name_kana='プロジェクトイチランテスト03',
            birthday=date.today(),
            gender=Gender.male,
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        engineer_history = EngineerHistory(
            engineer_id=engineer.id,
            payment_start_day=date(2016, 1, 1),
            payment_end_day=date(2018, 12, 31),
            payment_per_month=100,
            payment_site=Site.twenty_five,
            payment_tax=Tax.eight,
            payment_rule=Rule.variable,
            payment_bottom_base_hour=100,
            payment_top_base_hour=100,
            payment_free_base_hour='',
            payment_per_hour='1/100, 1/150',
            payment_per_bottom_hour=100,
            payment_per_top_hour=100,
            payment_fraction=Fraction.hundred,
            payment_fraction_rule=Round.down,
            payment_condition='test',
            remarks='test',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_history)
        db.session.commit()

        project = Project(
            project_name='プロジェクト一覧テスト03',
            project_name_for_bp='プロジェクト一覧テスト03',
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='プロジェクト一覧テスト03',
            end_user_company_id=company.id,
            client_company_id=company.id,
            start_date='2018/1/1',
            end_date='2018/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            billing_tax=Tax.zero,
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

        project_detail = ProjectDetail(
            project_id=project.id,
            detail_type=DetailType.engineer,
            work_name='プロジェクト一覧テスト03',
            engineer_id=engineer.id,
            billing_money=100,
            remarks='remarks',
            billing_start_day='2017/1/1',
            billing_end_day='2018/12/31',
            billing_per_month=100,
            billing_rule=Rule.variable,
            billing_bottom_base_hour=120,
            billing_top_base_hour=200,
            billing_free_base_hour='billing_free_base_hour',
            billing_per_hour='billing_per_hour',
            billing_per_bottom_hour=120,
            billing_per_top_hour=200,
            billing_fraction=Fraction.one,
            billing_fraction_rule=Round.down,
            bp_order_no='bp_order_no',
            client_order_no_for_bp='client_order_no_for_bp',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test', )
        db.session.add(project_detail)

        db.session.commit()

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.project_list.value,
            'month': date(2018, 8, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

    # 請求ルール・支払ルールが'変動'、かつ基準時間入力なしのテストケース
    def test_download_project_list_04(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # setup
        # 出力するデータがすべて入力されているケース作成
        company = Company(
            company_name='プロジェクト一覧テスト04',
            company_name_kana='プロジェクトイチランテスト04',
            company_short_name="プロテス04",
            contract_date=date.today(),
            postal_code='000-0000',
            address='住所',
            phone='000-0000',
            fax='000-0000',
            client_code='0001',
            bp_code='9999',
            billing_site=Site.twenty_five,
            payment_site=Site.thirty,
            billing_tax=Tax.zero,
            payment_tax=Tax.eight,
            bank_id='2',
            bank_holiday_flag=HolidayFlag.before,
            remarks='備考',
            print_name='印刷用宛名',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.bp,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='プロジェクト一覧テスト04',
            engineer_name_kana='プロジェクトイチランテスト04',
            birthday=date.today(),
            gender=Gender.male,
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        engineer_history = EngineerHistory(
            engineer_id=16,
            payment_start_day=date(2016, 1, 1),
            payment_end_day=date(2018, 12, 31),
            payment_per_month=100,
            payment_site=Site.twenty_five,
            payment_tax=Tax.eight,
            payment_rule=Rule.fixed,
            payment_bottom_base_hour=None,
            payment_top_base_hour=None,
            payment_free_base_hour='test',
            payment_per_hour='1/100, 1/150',
            payment_per_bottom_hour=100,
            payment_per_top_hour=100,
            payment_fraction=Fraction.hundred,
            payment_fraction_rule=Round.down,
            payment_condition='test',
            remarks='test',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_history)
        db.session.commit()

        project = Project(
            project_name='プロジェクト一覧テスト04',
            project_name_for_bp='プロジェクト一覧テスト04',
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='プロジェクト一覧テスト04',
            end_user_company_id=company.id,
            client_company_id=20,
            start_date='2018/1/1',
            end_date='2018/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            billing_tax=Tax.zero,
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

        project_detail = ProjectDetail(
            project_id=project.id,
            detail_type=DetailType.engineer,
            work_name='プロジェクト一覧テスト04',
            engineer_id=engineer.id,
            billing_money=100,
            remarks='remarks',
            billing_start_day='2017/1/1',
            billing_end_day='2018/12/31',
            billing_per_month=100,
            billing_rule=Rule.variable,
            billing_bottom_base_hour=None,
            billing_top_base_hour=None,
            billing_free_base_hour='billing_free_base_hour',
            billing_per_hour='billing_per_hour',
            billing_per_bottom_hour=120,
            billing_per_top_hour=200,
            billing_fraction=Fraction.one,
            billing_fraction_rule=Round.down,
            bp_order_no='bp_order_no',
            client_order_no_for_bp='client_order_no_for_bp',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test', )
        db.session.add(project_detail)

        db.session.commit()

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.project_list.value,
            'month': date(2018, 8, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

    # 請求ルール・支払ルールが'変動'、かつ基準時間入力なしのテストケース
    def test_download_project_list_05(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # setup
        # 出力するデータがすべて入力されているケース作成
        company = Company(
            company_name='プロジェクト一覧テスト05',
            company_name_kana='プロジェクトイチランテスト05',
            company_short_name="プロテス05",
            contract_date=date.today(),
            postal_code='000-0000',
            address='住所',
            phone='000-0000',
            fax='000-0000',
            client_code='0001',
            bp_code='9999',
            billing_site=Site.twenty_five,
            payment_site=Site.thirty,
            billing_tax=Tax.zero,
            payment_tax=Tax.eight,
            bank_id='2',
            bank_holiday_flag=HolidayFlag.before,
            remarks='備考',
            print_name='印刷用宛名',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.bp,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='プロジェクト一覧テスト05',
            engineer_name_kana='プロジェクトイチランテスト05',
            birthday=date.today(),
            gender=Gender.male,
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        # 範囲外の履歴を作成
        engineer_history = EngineerHistory(
            engineer_id=engineer.id,
            payment_start_day=date(2017, 1, 1),
            payment_end_day=date(2017, 12, 31),
            payment_per_month=100,
            payment_site=Site.twenty_five,
            payment_tax=Tax.eight,
            payment_rule=Rule.variable,
            payment_bottom_base_hour=None,
            payment_top_base_hour=None,
            payment_free_base_hour='history2',
            payment_per_hour='1/100, 1/150',
            payment_per_bottom_hour=100,
            payment_per_top_hour=100,
            payment_fraction=Fraction.hundred,
            payment_fraction_rule=Round.down,
            payment_condition='test',
            remarks='test',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_history)
        db.session.commit()

        # 範囲内の履歴を作成
        engineer_history = EngineerHistory(
            engineer_id=engineer.id,
            payment_start_day=date(2018, 1, 1),
            payment_end_day=date(2018, 12, 31),
            payment_per_month=100,
            payment_site=Site.twenty_five,
            payment_tax=Tax.eight,
            payment_rule=Rule.variable,
            payment_bottom_base_hour=None,
            payment_top_base_hour=None,
            payment_free_base_hour='test',
            payment_per_hour='1/100, 1/150',
            payment_per_bottom_hour=100,
            payment_per_top_hour=100,
            payment_fraction=Fraction.hundred,
            payment_fraction_rule=Round.down,
            payment_condition='test',
            remarks='test',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_history)
        db.session.commit()

        # 範囲外の履歴を作成
        engineer_history = EngineerHistory(
            engineer_id=engineer.id,
            payment_start_day=date(2019, 1, 1),
            payment_end_day=date(2019, 12, 31),
            payment_per_month=100,
            payment_site=Site.twenty_five,
            payment_tax=Tax.eight,
            payment_rule=Rule.variable,
            payment_bottom_base_hour=None,
            payment_top_base_hour=None,
            payment_free_base_hour='history2',
            payment_per_hour='1/100, 1/150',
            payment_per_bottom_hour=100,
            payment_per_top_hour=100,
            payment_fraction=Fraction.hundred,
            payment_fraction_rule=Round.down,
            payment_condition='test',
            remarks='test',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_history)
        db.session.commit()

        project = Project(
            project_name='プロジェクト一覧テスト05',
            project_name_for_bp='プロジェクト一覧テスト05',
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='プロジェクト一覧テスト05',
            end_user_company_id=21,
            client_company_id=21,
            start_date='2018/1/1',
            end_date='2018/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            billing_tax=Tax.zero,
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

        project_detail = ProjectDetail(
            project_id=project.id,
            detail_type=DetailType.engineer,
            work_name='プロジェクト一覧テスト05',
            engineer_id=engineer.id,
            billing_money=100,
            remarks='remarks',
            billing_start_day='2017/1/1',
            billing_end_day='2018/12/31',
            billing_per_month=100,
            billing_rule=Rule.variable,
            billing_bottom_base_hour=None,
            billing_top_base_hour=None,
            billing_free_base_hour='billing_free_base_hour',
            billing_per_hour='billing_per_hour',
            billing_per_bottom_hour=120,
            billing_per_top_hour=200,
            billing_fraction=Fraction.one,
            billing_fraction_rule=Round.down,
            bp_order_no='bp_order_no',
            client_order_no_for_bp='client_order_no_for_bp',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test', )
        db.session.add(project_detail)
        db.session.commit()

        # 範囲外の見積明細を作成
        project_detail = ProjectDetail(
            project_id=project.id,
            detail_type=DetailType.engineer,
            work_name='プロジェクト一覧テスト05_2',
            engineer_id=engineer.id,
            billing_money=100,
            remarks='remarks',
            billing_start_day='2019/1/1',
            billing_end_day='2019/12/31',
            billing_per_month=100,
            billing_rule=Rule.variable,
            billing_bottom_base_hour=None,
            billing_top_base_hour=None,
            billing_free_base_hour='billing_free_base_hour',
            billing_per_hour='billing_per_hour',
            billing_per_bottom_hour=120,
            billing_per_top_hour=200,
            billing_fraction=Fraction.one,
            billing_fraction_rule=Round.down,
            bp_order_no='bp_order_no',
            client_order_no_for_bp='client_order_no_for_bp',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test', )
        db.session.add(project_detail)
        db.session.commit()

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.project_list.value,
            'month': date(2018, 8, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

    # 契約範囲外のユーザーが登録されているケース
    def test_download_project_list_06(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # setup
        # 出力するデータがすべて入力されているケース作成
        company = Company(
            company_name='プロジェクト一覧テスト06',
            company_name_kana='プロジェクトイチランテスト06',
            company_short_name="プロテス06",
            contract_date=date.today(),
            postal_code='000-0000',
            address='住所',
            phone='000-0000',
            fax='000-0000',
            client_code='0001',
            bp_code='9999',
            billing_site=Site.twenty_five,
            payment_site=Site.thirty,
            billing_tax=Tax.zero,
            payment_tax=Tax.eight,
            bank_id='2',
            bank_holiday_flag=HolidayFlag.before,
            remarks='備考',
            print_name='印刷用宛名',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company)
        db.session.commit()

        company_client_flag = CompanyClientFlag(
            company_id=company.id,
            client_flag=ClientFlag.bp,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)
        db.session.commit()

        engineer = Engineer(
            engineer_name='プロジェクト一覧テスト06',
            engineer_name_kana='プロジェクトイチランテスト06',
            birthday=date.today(),
            gender=Gender.male,
            company_id=company.id,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer)
        db.session.commit()

        # 範囲外の履歴を作成
        engineer_history = EngineerHistory(
            engineer_id=engineer.id,
            payment_start_day=date(2017, 1, 1),
            payment_end_day=date(2017, 12, 31),
            payment_per_month=100,
            payment_site=Site.twenty_five,
            payment_tax=Tax.eight,
            payment_rule=Rule.variable,
            payment_bottom_base_hour=None,
            payment_top_base_hour=None,
            payment_free_base_hour='history2',
            payment_per_hour='1/100, 1/150',
            payment_per_bottom_hour=100,
            payment_per_top_hour=100,
            payment_fraction=Fraction.hundred,
            payment_fraction_rule=Round.down,
            payment_condition='test',
            remarks='test',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_history)
        db.session.commit()

        project = Project(
            project_name='プロジェクト一覧テスト06',
            project_name_for_bp='プロジェクト一覧テスト06',
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='プロジェクト一覧テスト06',
            end_user_company_id=21,
            client_company_id=21,
            start_date='2018/1/1',
            end_date='2018/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.billing_at_last,
            estimated_total_amount=1000000,
            billing_tax=Tax.zero,
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

        project_detail = ProjectDetail(
            project_id=project.id,
            detail_type=DetailType.engineer,
            work_name='プロジェクト一覧テスト06',
            engineer_id=engineer.id,
            billing_money=100,
            remarks='remarks',
            billing_start_day='2018/1/1',
            billing_end_day='2018/12/31',
            billing_per_month=100,
            billing_rule=Rule.variable,
            billing_bottom_base_hour=None,
            billing_top_base_hour=None,
            billing_free_base_hour='billing_free_base_hour',
            billing_per_hour='billing_per_hour',
            billing_per_bottom_hour=120,
            billing_per_top_hour=200,
            billing_fraction=Fraction.one,
            billing_fraction_rule=Round.down,
            bp_order_no='bp_order_no',
            client_order_no_for_bp='client_order_no_for_bp',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test', )
        db.session.add(project_detail)
        db.session.commit()

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.project_list.value,
            'month': date(2018, 8, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

    # 出力項目のデータが存在するケース
    def test_download_billing_list1(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # setup
        for num in range(2):
            company = Company(
                company_name='請求一覧テスト01',
                company_name_kana='セイキュウイチランテスト01',
                company_short_name="テス01",
                contract_date=date.today(),
                postal_code='000-0000',
                address='住所',
                phone='000-0000',
                fax='000-0000',
                client_code='0001',
                bp_code='9999',
                billing_site=Site.twenty_five,
                payment_site=Site.thirty,
                billing_tax=Tax.zero,
                payment_tax=Tax.eight,
                bank_id='2',
                bank_holiday_flag=HolidayFlag.before,
                remarks='備考',
                print_name='印刷用宛名',
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
            db.session.add(company)

            project = Project(
                project_name='請求一覧テスト01',
                project_name_for_bp='セイキュウ一覧テスト01',
                status=Status.start,
                recorded_department_id=1,
                sales_person='営業担当',
                estimation_no='請求一覧テスト01' + str(num),
                end_user_company_id=13 + num,
                client_company_id=13 + num,
                start_date='2018/1/1',
                end_date='2018/12/31',
                contract_form=Contract.blanket,
                billing_timing=BillingTiming.billing_at_last,
                estimated_total_amount=1000000,
                billing_tax=Tax.zero,
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

            project_month = ProjectMonth(
                project_id=13 + num,
                project_month='2017/1/1',
                billing_input_flag=InputFlag.yet,
                deposit_input_flag=InputFlag.yet,
                billing_printed_date='2017/1/1',
                deposit_date='2017/1/1',
                billing_estimated_money=120,
                billing_confirmation_money=120,
                billing_tax=Tax.eight,
                billing_transportation=120,
                remarks='remarks',
                client_billing_no=1005 + num,
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
            db.session.add(project_month)

            db.session.commit()

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.billing_list.value,
            'month': date(2017, 1, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

    # 部署・本部が変わったパターンのテストケース
    def test_download_billing_list2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # setup
        for num in range(2):
            company = Company(
                company_name='請求一覧テスト01',
                company_name_kana='セイキュウイチランテスト01',
                company_short_name="テス01",
                contract_date=date.today(),
                postal_code='000-0000',
                address='住所',
                phone='000-0000',
                fax='000-0000',
                client_code='0001',
                bp_code='9999',
                billing_site=Site.twenty_five,
                payment_site=Site.thirty,
                billing_tax=Tax.zero,
                payment_tax=Tax.eight,
                bank_id='2',
                bank_holiday_flag=HolidayFlag.before,
                remarks='備考',
                print_name='印刷用宛名',
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
            db.session.add(company)

            project = Project(
                project_name='請求一覧テスト01',
                project_name_for_bp='セイキュウ一覧テスト01',
                status=Status.start,
                recorded_department_id=2,
                sales_person='営業担当',
                estimation_no='請求一覧テスト02' + str(num),
                end_user_company_id=15 + num,
                client_company_id=15 + num,
                start_date='2018/1/1',
                end_date='2018/12/31',
                contract_form=Contract.blanket,
                billing_timing=BillingTiming.billing_at_last,
                estimated_total_amount=1000000,
                billing_tax=Tax.zero,
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

            project_month = ProjectMonth(
                project_id=15 + num,
                project_month='2017/1/1',
                billing_input_flag=InputFlag.yet,
                deposit_input_flag=InputFlag.yet,
                billing_printed_date='2017/1/1',
                deposit_date='2017/1/1',
                billing_estimated_money=120,
                billing_confirmation_money=120,
                billing_tax=Tax.eight,
                billing_transportation=120,
                remarks='remarks',
                client_billing_no=1007 + num,
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
            db.session.add(project_month)

            db.session.commit()

        # 帳票DL実施
        result = self.app.post('/output/', data={
            'output_report': OutputType.billing_list.value,
            'month': date(2017, 1, 1).strftime('%Y/%m')
        })
        self.assertEqual(result.status_code, 200)

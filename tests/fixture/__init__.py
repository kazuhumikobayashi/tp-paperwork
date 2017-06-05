from datetime import datetime, date, timedelta

from application import bcrypt, db
from application.domain.model.attachment import Attachment
from application.domain.model.company import Company
from application.domain.model.department import Department
from application.domain.model.engineer import Engineer
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.expression import Expression
from application.domain.model.immutables.gender import Gender
from application.domain.model.immutables.holiday_flag import HolidayFlag
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.project_attachment_type import ProjectAttachmentType
from application.domain.model.immutables.round import Round
from application.domain.model.immutables.site import Site
from application.domain.model.immutables.status import Status
from application.domain.model.immutables.tax import Tax
from application.domain.model.project import Project
from application.domain.model.project_attachment import ProjectAttachment
from application.domain.model.project_detail import ProjectDetail
from application.domain.model.skill import Skill
from application.domain.model.business_category import BusinessCategory
from application.domain.model.user import User
from application.domain.model.bank import Bank
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.engineer_history import EngineerHistory


def init_data():
    # マスターデータの作成
    create_user()
    create_skills()
    create_banks()
    create_companies()
    create_engineers()
    create_departments()
    create_projects()
    create_attachments()
    create_business_categories()
    create_company_client_flags()
    create_engineer_histories()
    create_project_details()


def create_user():
    for num in range(12):
        user = User(
                 shain_number='test' + str(num),
                 user_name='単体テスト',
                 password=bcrypt.generate_password_hash('test'),
                 created_at=datetime.today(),
                 created_user='test',
                 updated_at=datetime.today(),
                 updated_user='test')
        db.session.add(user)
    db.session.commit()


def create_skills():
    for num in range(12):
        skill = Skill(
            skill_name='test' + str(num),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(skill)
    db.session.commit()


def create_companies():
    for num in range(12):
        company = Company(
                 company_name='test' + str(num),
                 company_name_kana='タンタイテスト',
                 company_short_name="単テス",
                 contract_date=date.today(),
                 postal_code='000-0000',
                 address='住所',
                 phone='000-0000',
                 fax='000-0000',
                 client_code='0001',
                 bp_code='9999',
                 payment_site=Site.twenty_five,
                 receipt_site=Site.thirty,
                 payment_tax=Tax.zero,
                 receipt_tax=Tax.eight,
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


def create_engineers():
    for num in range(12):
        engineer = Engineer(
                engineer_name='test' + str(num),
                engineer_name_kana='テスト' + str(num),
                birthday=date.today(),
                gender=Gender.male,
                company_id=num+1,
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
        db.session.add(engineer)
    db.session.commit()


def create_departments():
    for num in range(12):
        department = Department(
            group_name='本部' + str(num),
            department_name='単体テスト' + str(num),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(department)
    db.session.commit()


def create_projects():
    for num in range(12):
        project = Project(
            project_name='単体テスト' + str(num),
            project_name_for_bp='テスト' + str(num),
            status=Status.start,
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='test' + str(num),
            end_user_company_id=1,
            client_company_id=5,
            start_date=date.today(),
            end_date='2099/12/31',
            contract_form=Contract.blanket,
            billing_timing=BillingTiming.payment_at_last,
            estimated_total_amount=1000000,
            deposit_date='2099/12/31',
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


def create_attachments():
    for num in range(2):
        attachment = Attachment(
            filename='見積書' + str(num) + '.pdf',
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
            remarks='remarks' + str(num),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project_attachment)
        db.session.commit()


def create_business_categories():
    for num in range(12):
        business_category = BusinessCategory(
            business_category_name='test' + str(num),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(business_category)
    db.session.commit()


def create_banks():
    for num in range(12):
        bank = Bank(
                 bank_name='test' + str(num),
                 text_for_document='単体テスト',
                 created_at=datetime.today(),
                 created_user='test',
                 updated_at=datetime.today(),
                 updated_user='test')
        db.session.add(bank)
    db.session.commit()


def create_company_client_flags():
    for num in range(4):
        company_client_flag = CompanyClientFlag(
            company_id=num+1,
            client_flag=ClientFlag.parse(num+1),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)    
    db.session.commit()


def create_engineer_histories():
    for num in range(5):
        engineer_history = EngineerHistory(
            engineer_id=1,
            receipt_start_day=date(2016, 2*num+1, 1),
            receipt_end_day=date(2016, 2*num+3, 1)-timedelta(days=1),
            receipt_per_month=num+1,
            receipt_rule=1,
            receipt_bottom_base_hour=num+1,
            receipt_top_base_hour=num+2,
            receipt_free_base_hour='',
            receipt_per_hour='1/100, 1/150',
            receipt_per_bottom_hour=num+1,
            receipt_per_top_hour=num+2,
            receipt_fraction=100,
            receipt_fraction_calculation1=Expression.more,
            receipt_fraction_calculation2=Round.up,
            receipt_condition='test' + str(num),
            remarks='test' + str(num),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_history)    
    db.session.commit()


def create_project_details():
    for num in range(5):
        project_detail = ProjectDetail(
            project_id=1,
            detail_type=DetailType.engineer,
            work_name=None,
            engineer_id=num+1,
            payment_money=1000000,
            remarks='テスト',
            payment_start_day=date(2016, 7, 1),
            payment_end_day=date(2016, 12, 1),
            payment_per_month=700000,
            payment_rule=Rule.fixed,
            payment_bottom_base_hour=num+2,
            payment_top_base_hour=100,
            payment_free_base_hour='1/100, 1/150',
            payment_per_hour=1,
            payment_per_bottom_hour=num+1,
            payment_per_top_hour=num+1,
            payment_fraction=100,
            payment_fraction_calculation1=1,
            payment_fraction_calculation2=1,
            bp_order_no=None,
            client_order_no_for_bp=None,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(project_detail)
    db.session.commit()

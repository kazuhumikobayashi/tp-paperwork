from datetime import datetime, date

from application import bcrypt, db
from application.domain.model.assigned_members import AssignedMember
from application.domain.model.attachment import Attachment
from application.domain.model.billing import Billing
from application.domain.model.company import Company
from application.domain.model.department import Department
from application.domain.model.engineer import Engineer
from application.domain.model.engineer_actual_result import EngineerActualResult
from application.domain.model.estimation_remarks import EstimationRemarks
from application.domain.model.order_remarks import OrderRemarks
from application.domain.model.project import Project
from application.domain.model.project_attachment import ProjectAttachment
from application.domain.model.skill import Skill
from application.domain.model.business_category import BusinessCategory
from application.domain.model.user import User
from application.domain.model.bank import Bank
from application.domain.model.client_flag import ClientFlag
from application.domain.model.company_client_flag import CompanyClientFlag


def init_data():
    # マスターデータの作成
    create_user()
    create_skills()
    create_companies()
    create_engineers()
    create_departments()
    create_projects()
    create_attachments()
    create_business_categories()
    create_banks()
    create_client_flags()
    create_company_client_flags()


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
                 payment_site='10',
                 receipt_site='30',
                 payment_tax='0',
                 receipt_tax='8',
                 remarks='備考',
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
                gender='男性',
                company_id='1',
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
            status='01:契約開始',
            recorded_department_id=1,
            sales_person='営業担当',
            estimation_no='test' + str(num),
            end_user_company_id=1,
            client_company_id=5,
            start_date=date.today(),
            end_date='2099/12/31',
            contract_form='請負契約（一括契約）',
            billing_timing='契約期間末1回',
            estimated_total_amount=1000000,
            deposit_date='2099/12/31',
            scope='test',
            contents=None,
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

        estimation_remarks = EstimationRemarks(
            project_id=project.id,
            scope='scope',
            contents='contents',
            deliverables='deliverables',
            delivery_place='delivery_place',
            inspection_date='2017/1/1',
            responsible_person='responsible_person',
            quality_control='quality_control',
            subcontractor='subcontractor',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')

        order_remarks = OrderRemarks(
            project_id=project.id,
            order_no='1',
            order_amount=1,
            contents='contents',
            responsible_person='responsible_person',
            subcontractor='subcontractor',
            scope='scope',
            work_place='work_place',
            delivery_place='delivery_place',
            deliverables='deliverables',
            inspection_date='2017/1/1',
            payment_terms='payment_terms',
            billing_company_id=1,
            remarks='remarks',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')

        assigned_members = \
            [
                AssignedMember(
                    project_id=project.id,
                    seq_no=1,
                    engineer_id=1,
                    sales_unit_price=1,
                    payment_unit_price=1,
                    start_date=date.today().strftime('%Y/%m/%d'),
                    end_date='2099/12/31',
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test'),
                AssignedMember(
                    project_id=project.id,
                    seq_no=1,
                    engineer_id=2,
                    sales_unit_price=1,
                    payment_unit_price=1,
                    start_date=date.today().strftime('%Y/%m/%d'),
                    end_date='2099/12/31',
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')
            ]

        # 請求を登録
        billings = \
            [
                Billing(
                    project_id=project.id,
                    billing_month=date.today().strftime('%Y/%m/%d'),
                    billing_amount=1,
                    billing_adjustment_amount=1,
                    tax=1,
                    carfare=1,
                    scheduled_billing_date=date.today().strftime('%Y/%m/%d'),
                    billing_date=date.today().strftime('%Y/%m/%d'),
                    bill_output_date=date.today().strftime('%Y/%m/%d'),
                    scheduled_payment_date=date.today().strftime('%Y/%m/%d'),
                    payment_date=date.today().strftime('%Y/%m/%d'),
                    status=1,
                    remarks='remarks',
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test'),
                Billing(
                    project_id=project.id,
                    billing_month=date.today().strftime('%Y/%m/%d'),
                    billing_amount=2,
                    billing_adjustment_amount=2,
                    tax=2,
                    carfare=2,
                    scheduled_billing_date=date.today().strftime('%Y/%m/%d'),
                    billing_date=date.today().strftime('%Y/%m/%d'),
                    bill_output_date=date.today().strftime('%Y/%m/%d'),
                    scheduled_payment_date=date.today().strftime('%Y/%m/%d'),
                    payment_date=date.today().strftime('%Y/%m/%d'),
                    status=None,
                    remarks='remarks',
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')
            ]

        engineer_actual_results = \
            [
                EngineerActualResult(
                    project_id=1,
                    result_month=date.today().strftime('%Y/%m/%d'),
                    seq_no=1,
                    engineer_id=1,
                    fixed_flg='1',
                    working_hours=1,
                    adjustment_hours=1,
                    billing_amount=1,
                    billing_adjustment_amount=1,
                    payment_amount=1,
                    payment_adjustment_amount=1,
                    carfare=1,
                    remarks='remarks',
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test'),
                EngineerActualResult(
                    project_id=project.id,
                    result_month=date.today().strftime('%Y/%m/%d'),
                    seq_no=2,
                    engineer_id=2,
                    fixed_flg='2',
                    working_hours=2,
                    adjustment_hours=2,
                    billing_amount=2,
                    billing_adjustment_amount=2,
                    payment_amount=2,
                    payment_adjustment_amount=2,
                    carfare=2,
                    remarks=None,
                    created_at=datetime.today(),
                    created_user='test',
                    updated_at=datetime.today(),
                    updated_user='test')
            ]

        project.estimation_remarks = estimation_remarks
        project.order_remarks = order_remarks
        project.assigned_members = assigned_members
        project.billings = billings
        project.engineer_actual_results = engineer_actual_results

        db.session.add(project)
    db.session.commit()


def create_attachments():
    attachment = Attachment(
        filename='見積書.pdf',
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


def create_client_flags():
    client_flag_names = ['自社', 'BP所属', '顧客', 'エンドユーザー']
    for client_flag_name in client_flag_names:
        client_flag = ClientFlag(
            client_flag_name=client_flag_name,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(client_flag)
    db.session.commit()


def create_company_client_flags():
    for num in range(4):
        company_client_flag = CompanyClientFlag(
            company_id=num+1,
            client_flag_id=num+1,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(company_client_flag)    
    db.session.commit()

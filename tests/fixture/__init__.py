from datetime import datetime, date

from application import bcrypt, db
from application.domain.model.assigned_members import AssignedMember
from application.domain.model.attachment import Attachment
from application.domain.model.billing import Billing
from application.domain.model.calculation import Calculation
from application.domain.model.company import Company
from application.domain.model.contract_form import ContractForm
from application.domain.model.department import Department
from application.domain.model.engineer import Engineer
from application.domain.model.engineer_actual_result import EngineerActualResult
from application.domain.model.estimation_remarks import EstimationRemarks
from application.domain.model.order_remarks import OrderRemarks
from application.domain.model.project import Project
from application.domain.model.project_attachment import ProjectAttachment
from application.domain.model.skill import Skill
from application.domain.model.business_category import BusinessCategory
from application.domain.model.status import Status
from application.domain.model.tax import Tax
from application.domain.model.user import User


def init_data():
    # マスターデータの作成
    create_user()
    create_taxes()
    create_skills()
    create_companies()
    create_engineers()
    create_departments()
    create_calculations()
    create_statuses()
    create_contract_forms()
    create_projects()
    create_attachments()
    create_business_categories()


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


def create_taxes():
    for num in range(12):
        tax = Tax(
            start_date=date.today(),
            end_date='2099/12/31',
            tax_rate=num,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(tax)
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
                 company_code='test' + str(num),
                 company_name='単体テスト',
                 client_flg='1',
                 consignment_flg='1',
                 start_date=date.today(),
                 end_date='2099/12/31',
                 tax='1',
                 created_at=datetime.today(),
                 created_user='test',
                 updated_at=datetime.today(),
                 updated_user='test')
        db.session.add(company)
    db.session.commit()


def create_engineers():
    for num in range(12):
        engineer = Engineer(
                start_date=date.today(),
                end_date='2099/12/31',
                engineer_name='単体テスト',
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
            department_name='単体テスト' + str(num),
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(department)
    db.session.commit()


def create_calculations():
    for num in range(12):
        calculation = Calculation(
            calculation_name='単体テスト' + str(num),
            amount=num,
            formula=1,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(calculation)
    db.session.commit()


def create_statuses():
    statuses = ['見積り中', '受注済', '完了', '失注']
    for status_name in statuses:
        status = Status(
            status_name=status_name,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(status)
    db.session.commit()


def create_contract_forms():
    contract_forms = ['一括', '準委任', '派遣']
    for contract_form_name in contract_forms:
        contract_form = ContractForm(
            contract_form_name=contract_form_name,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(contract_form)
    db.session.commit()


def create_projects():
    for num in range(12):
        project = Project(
            project_name='単体テスト' + str(num),
            end_user='test',
            client_company_id=1,
            start_date=date.today(),
            end_date='2099/12/31',
            recorded_department_id=1,
            over_time_calculation_id=1,
            contract_form_id=1,
            estimation_no='test' + str(num),
            status_id=1,
            billing_timing='1',
            remarks='test',
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

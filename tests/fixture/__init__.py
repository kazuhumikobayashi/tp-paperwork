from datetime import datetime, date

from application import bcrypt, db
from application.domain.model.calculation import Calculation
from application.domain.model.company import Company
from application.domain.model.contract_form import ContractForm
from application.domain.model.department import Department
from application.domain.model.engineer import Engineer
from application.domain.model.skill import Skill
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


def create_user():
    for num in range(12):
        user = User(
                 shain_number='test' + str(num),
                 user_name='単体テスト',
                 mail='test@test' + str(num) + '.com',
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
            department_code='test' + str(num),
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

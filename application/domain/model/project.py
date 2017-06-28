from datetime import date, datetime

from flask import session

from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.company import Company
from application.domain.model.department import Department
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.contract import Contract
from application.domain.model.immutables.status import Status
from application.domain.model.project_attachment import ProjectAttachment
from application.domain.model.project_month import ProjectMonth
from application.domain.model.project_detail import ProjectDetail
from application.domain.model.sqlalchemy.types import EnumType
from application.service.calculator import Calculator


class Project(BaseModel, db.Model):
    __tablename__ = 'projects'
    PER_PAGE = 10

    project_name = Column(String(128), nullable=False)
    project_name_for_bp = Column(String(128))
    status = Column(EnumType(enum_class=Status), nullable=False, default=1)
    recorded_department_id = Column(Integer, ForeignKey("departments.id"))
    sales_person = Column(String(128))
    estimation_no = Column(String(64), unique=True)
    end_user_company_id = Column(Integer, ForeignKey("companies.id"))
    client_company_id = Column(Integer, ForeignKey("companies.id"))
    _start_date = Column('start_date', Date, nullable=False)
    end_date = Column(Date, nullable=False)
    contract_form = Column(EnumType(enum_class=Contract))
    billing_timing = Column(EnumType(enum_class=BillingTiming))
    estimated_total_amount = Column(Integer)
    scope = Column(String(1024))
    contents = Column(String(1024))
    working_place = Column(String(1024))
    delivery_place = Column(String(1024))
    deliverables = Column(String(1024))
    inspection_date = Column(Date)
    responsible_person = Column(String(128))
    quality_control = Column(String(128))
    subcontractor = Column(String(128))
    remarks = Column(String(1024))
    client_order_no = Column(String(64))

    end_user_company = relationship(Company, lazy='joined', foreign_keys=[end_user_company_id])
    client_company = relationship(Company, lazy='joined', foreign_keys=[client_company_id])
    recorded_department = relationship(Department, lazy='joined')
    project_attachments = relationship(ProjectAttachment, cascade='all, delete-orphan')
    project_details = relationship(ProjectDetail, cascade='all, delete-orphan')
    project_months = relationship(ProjectMonth,
                                  order_by="desc(ProjectMonth.project_month)",
                                  cascade='all, delete-orphan')

    _is_start_date_change = False

    @hybrid_property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        old = self._get_fiscal_year(self._start_date)
        new = self._get_fiscal_year(value)

        if old != new:
            self._is_start_date_change = True
        self._start_date = value

    @property
    def is_start_date_change(self):
        if not self.id:
            return True
        return self._is_start_date_change

    def __init__(self,
                 project_name=None,
                 project_name_for_bp=None,
                 status=Status.start,
                 recorded_department_id=None,
                 sales_person=None,
                 estimation_no=None,
                 end_user_company_id=None,
                 client_company_id=None,
                 start_date=None,
                 end_date=None,
                 contract_form=None,
                 billing_timing=None,
                 estimated_total_amount=None,
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
                 client_order_no=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Project, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_name = project_name
        self.project_name_for_bp = project_name_for_bp
        self.status = status
        self.recorded_department_id = recorded_department_id
        self.sales_person = sales_person
        self.estimation_no = estimation_no
        self.end_user_company_id = end_user_company_id
        self.client_company_id = client_company_id
        self._start_date = start_date
        self.end_date = end_date
        self.contract_form = contract_form
        self.billing_timing = billing_timing
        self.estimated_total_amount = estimated_total_amount
        self.scope = scope
        self.contents = contents
        self.working_place = working_place
        self.delivery_place = delivery_place
        self.deliverables = deliverables
        self.inspection_date = inspection_date
        self.responsible_person = responsible_person
        self.quality_control = quality_control
        self.subcontractor = subcontractor
        self.remarks = remarks
        self.client_order_no = client_order_no

    def get_fiscal_year(self):
        return self._get_fiscal_year(self.start_date)

    def get_project_attachments(self):
        tmp = sorted(self.project_attachments,
                     key=lambda project_attachment: project_attachment.type.value)
        project_attachments = attachments = []
        old_type = None
        for attachment in tmp:
            if old_type == attachment.type.value:
                attachments += [attachment]
            else:
                attachments = [attachment]
                project_attachments += [{"type": attachment.type.name, "attachments": attachments}]
                old_type = attachment.type.value
        return project_attachments

    @staticmethod
    def _get_fiscal_year(date_):
        if not date_:
            return None
        if int(date_.strftime('%m')) >= 10:
            return int(date_.strftime('%y')) + 1
        else:
            return int(date_.strftime('%y'))

    # 開始・終了日のそれぞれの年月をリストで返すメソッド
    def get_project_month_list(self):
        project_month_list = []
        i = 0
        start = self.start_date
        while (date(start.year, start.month, 1) + relativedelta(months=i)) <= self.end_date:
            project_month_list.append(date(start.year, start.month, 1) + relativedelta(months=i))
            i += 1
        return project_month_list

    # 見積もり合計金額を月々で割った値を取得
    def get_estimated_total_amount_by_month(self):
        return self.estimated_total_amount / len(self.get_project_month_list())

    # プロジェクトの年月情報を作成
    def create_project_months(self):
        project_dates = self.get_project_month_list()
        for project_date in project_dates:
            calculator = Calculator(
                            project_date,
                            self.client_company.billing_site,
                            self.client_company.bank_holiday_flag)
            project_month = ProjectMonth(
                                project_month=project_date,
                                deposit_date=calculator.get_deposit_date(),
                                created_at=datetime.today(),
                                created_user=session['user']['user_name'],
                                updated_at=datetime.today(),
                                updated_user=session['user']['user_name'])
            if self.billing_timing == BillingTiming.billing_by_month:
                project_month.billing_estimated_money = self.get_estimated_total_amount_by_month()
            else:
                if project_date == max(project_dates):
                    project_month.billing_estimated_money = self.estimated_total_amount
            self.project_months.append(project_month)
        return self

    def has_not_project_results(self):
        for project_detail in self.project_details:
            if project_detail.project_results:
                return False
        return True

    def has_not_project_billings(self):
        for project_detail in self.project_details:
            if project_detail.project_billings:
                return False
        return True

    def has_not_project_months(self):
        return not self.project_months

    def has_payment(self):
        return True in [project_detail.has_payment() for project_detail in self.project_details]

    def tax_of_estimated_total_amount(self):
        if self.client_company:
            return self.estimated_total_amount * self.client_company.billing_tax.rate
        else:
            return 0

    def __repr__(self):
        return "<Project:" + \
                "'id='{}".format(self.id) + \
                "', project_name='{}".format(self.project_name) + \
                "', project_name_for_bp='{}".format(self.project_name_for_bp) + \
                "', status='{}".format(self.status) + \
                "', recorded_department_id='{}".format(self.recorded_department_id) + \
                "', sales_person='{}".format(self.sales_person) + \
                "', estimation_no='{}".format(self.estimation_no) + \
                "', end_user_company_id='{}".format(self.end_user_company_id) + \
                "', client_company_id='{}".format(self.client_company_id) + \
                "', start_date='{}".format(self.start_date) + \
                "', end_date='{}".format(self.end_date) + \
                "', contract_form='{}".format(self.contract_form) + \
                "', billing_timing='{}".format(self.billing_timing) + \
                "', estimated_total_amount='{}".format(self.estimated_total_amount) + \
                "', scope='{}".format(self.scope) + \
                "', contents='{}".format(self.contents) + \
                "', working_place='{}".format(self.working_place) + \
                "', delivery_place='{}".format(self.delivery_place) + \
                "', deliverables='{}".format(self.deliverables) + \
                "', inspection_date='{}".format(self.inspection_date) + \
                "', responsible_person='{}".format(self.responsible_person) + \
                "', quality_control='{}".format(self.quality_control) + \
                "', subcontractor='{}".format(self.subcontractor) + \
                "', remarks='{}".format(self.remarks) + \
                "', client_order_no='{}".format(self.client_order_no) + \
                "', project_attachments='{}".format(self.project_attachments) + \
                "', project_months='{}".format(self.project_months) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

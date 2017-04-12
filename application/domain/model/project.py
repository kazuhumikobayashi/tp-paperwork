from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.const import PROJECT_ATTACHMENT_TYPE
from application.domain.model.assigned_members import AssignedMember
from application.domain.model.base_model import BaseModel
from application.domain.model.billing import Billing
from application.domain.model.company import Company
from application.domain.model.contract_form import ContractForm
from application.domain.model.department import Department
from application.domain.model.engineer_actual_result import EngineerActualResult
from application.domain.model.estimation_remarks import EstimationRemarks
from application.domain.model.order_remarks import OrderRemarks
from application.domain.model.payment import Payment
from application.domain.model.project_attachment import ProjectAttachment
from application.domain.model.status import Status


class Project(BaseModel, db.Model):
    __tablename__ = 'projects'
    PER_PAGE = 10

    project_name = Column(String(128), nullable=False)
    end_user = Column(String(128))
    client_company_id = Column(Integer, ForeignKey("companies.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    recorded_department_id = Column(Integer, ForeignKey("departments.id"))
    over_time_calculation_id = Column(Integer, nullable=False)
    contract_form_id = Column(Integer, ForeignKey("contract_forms.id"), nullable=False)
    estimation_no = Column(String(64), nullable=False, unique=True)
    status_id = Column(Integer, ForeignKey("statuses.id"), nullable=False)
    billing_timing = Column(String(1), nullable=False)
    remarks = Column(String(1024))

    client_company = relationship(Company, lazy='joined')
    recorded_department = relationship(Department, lazy='joined')
    status = relationship(Status, lazy='joined')
    contract_form = relationship(ContractForm, lazy='joined')
    assigned_members = relationship(AssignedMember, cascade='all, delete-orphan')
    estimation_remarks = relationship(EstimationRemarks, cascade='all, delete-orphan', uselist=False)
    order_remarks = relationship(OrderRemarks, cascade='all, delete-orphan', uselist=False)
    engineer_actual_results = relationship(EngineerActualResult, cascade='all, delete-orphan')
    project_attachments = relationship(ProjectAttachment, cascade='all, delete-orphan')
    billings = relationship(Billing, cascade='all, delete-orphan')
    payments = relationship(Payment, cascade='all, delete-orphan')

    is_start_date_change = False

    def __init__(self,
                 project_name=None,
                 end_user=None,
                 client_company_id=None,
                 start_date=None,
                 end_date=None,
                 recorded_department_id=None,
                 over_time_calculation_id=None,
                 contract_form_id=None,
                 estimation_no=None,
                 status_id=None,
                 billing_timing=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Project, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_name = project_name
        self.end_user = end_user
        self.client_company_id = client_company_id
        self.start_date = start_date
        self.end_date = end_date
        self.recorded_department_id = recorded_department_id
        self.over_time_calculation_id = over_time_calculation_id
        self.contract_form_id = contract_form_id
        self.estimation_no = estimation_no
        self.status_id = status_id
        self.billing_timing = billing_timing
        self.remarks = remarks
        self.is_start_date_change = True

    def __repr__(self):
        return "<Project:" + \
                "'id='{}".format(self.id) + \
                "', project_name='{}".format(self.project_name) + \
                "', end_user='{}".format(self.end_user) + \
                "', client_company='{}".format(self.client_company) + \
                "', start_date='{}".format(self.start_date) + \
                "', end_date='{}".format(self.end_date) + \
                "', recorded_department='{}".format(self.recorded_department) + \
                "', over_time_calculation_id='{}".format(self.over_time_calculation_id) + \
                "', contract_form='{}".format(self.contract_form) + \
                "', estimation_no='{}".format(self.estimation_no) + \
                "', status='{}".format(self.status) + \
                "', billing_timing='{}".format(self.billing_timing) + \
                "', remarks='{}".format(self.remarks) + \
                "', assigned_members='{}".format(self.assigned_members) + \
                "', estimation_remarks='{}".format(self.estimation_remarks) + \
                "', order_remarks='{}".format(self.order_remarks) + \
                "', engineer_actual_results='{}".format(self.engineer_actual_results) + \
                "', project_attachments='{}".format(self.project_attachments) + \
                "', billings='{}".format(self.billings) + \
                "', payments='{}".format(self.payments) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

    def clone(self):
        arguments = dict()
        copy = Project()
        for name, column in self.__mapper__.columns.items():
            if not (column.primary_key or column.unique):
                arguments[name] = getattr(self, name)
        return copy.__class__(**arguments)

    def get_engineer_actual_results(self):
        tmp = sorted(self.engineer_actual_results,
                     key=lambda engineer_actual_result: engineer_actual_result.result_month)
        engineer_actual_results = results = []
        old_month = None
        for result in tmp:
            if old_month == result.result_month:
                results += [result]
            else:
                results = [result]
                engineer_actual_results += [(result.result_month, results)]
            old_month = result.result_month
        return engineer_actual_results

    def get_billings(self):
        tmp = sorted(self.billings,
                     key=lambda billing: billing.billing_month)
        billings = results = []
        old_month = None
        for result in tmp:
            if old_month == result.billing_month:
                results += [result]
            else:
                results = [result]
                billings += [(result.billing_month, results)]
            old_month = result.billing_month
        return billings

    def get_fiscal_year(self):
        if int(self.start_date.strftime('%m')) >= 10:
            return int(self.start_date.strftime('%y')) + 1
        else:
            return int(self.start_date.strftime('%y'))

    def get_project_attachments(self):
        tmp = sorted(self.project_attachments,
                     key=lambda project_attachment: project_attachment.type)
        project_attachments = attachments = []
        old_type = None
        for attachment in tmp:
            if old_type == attachment.type:
                attachments += [attachment]
            else:
                attachments = [attachment]
                project_attachments += [{"type": PROJECT_ATTACHMENT_TYPE[attachment.type], "attachments": attachments}]
                old_type = attachment.type
        return project_attachments

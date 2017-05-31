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
from application.domain.model.sqlalchemy.types import EnumType


class Project(BaseModel, db.Model):
    __tablename__ = 'projects'
    PER_PAGE = 10

    project_name = Column(String(128), nullable=False)
    project_name_for_bp = Column(String(128))
    status = Column(EnumType(enum_class=Status))
    recorded_department_id = Column(Integer, ForeignKey("departments.id"))
    sales_person = Column(String(128))
    estimation_no = Column(String(64), unique=True)
    end_user_company_id = Column(Integer, ForeignKey("companies.id"))
    client_company_id = Column(Integer, ForeignKey("companies.id"))
    _start_date = Column('start_date', Date)
    end_date = Column(Date)
    contract_form = Column(EnumType(enum_class=Contract))
    billing_timing = Column(EnumType(enum_class=BillingTiming))
    estimated_total_amount = Column(Integer)
    deposit_date = Column(Date)
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

    _is_start_date_change = False

    @hybrid_property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        if self.start_date and self.start_date != value:
            self._is_start_date_change = True
        self._start_date = value

    @property
    def is_start_date_change(self):
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
                 deposit_date=None,
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
        self.deposit_date = deposit_date
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
                "', deposit_date='{}".format(self.deposit_date) + \
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
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

    def clone(self):
        arguments = dict()
        copy = Project()
        for name, column in self.__mapper__.columns.items():
            if name[0:1] == '_':
                name = name[1:]
            if not (column.primary_key or column.unique):
                arguments[name] = getattr(self, name)
        return copy.__class__(**arguments)

    def get_fiscal_year(self):
        if int(self.start_date.strftime('%m')) >= 10:
            return int(self.start_date.strftime('%y')) + 1
        else:
            return int(self.start_date.strftime('%y'))

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

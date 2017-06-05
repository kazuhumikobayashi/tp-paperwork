from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.rule import Rule
from application.domain.model.sqlalchemy.types import EnumType


class ProjectDetail(BaseModel, db.Model):
    __tablename__ = 'project_details'
    PER_PAGE = 10

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    detail_type = Column(EnumType(enum_class=DetailType), nullable=False)
    work_name = Column(String(128))
    engineer_id = Column(Integer, ForeignKey("engineers.id"))
    payment_money = Column(Integer)
    remarks = Column(String(1024))
    payment_start_day = Column(Date)
    payment_end_day = Column(Date)
    payment_per_month = Column(Integer)
    payment_rule = Column(EnumType(enum_class=Rule))
    payment_bottom_base_hour = Column(Integer)
    payment_top_base_hour = Column(Integer)
    payment_free_base_hour = Column(String(128))
    payment_per_hour = Column(String(128))
    payment_per_bottom_hour = Column(Integer)
    payment_per_top_hour = Column(Integer)
    payment_fraction = Column(Integer)
    payment_fraction_calculation1 = Column(Integer)
    payment_fraction_calculation2 = Column(Integer)
    bp_order_no = Column(String(128))
    client_order_no_for_bp = Column(String(128))

    engineer = relationship("Engineer", lazy='joined')
    project = relationship("Project", lazy='joined')

    def __init__(self,
                 project_id=None,
                 detail_type=None,
                 work_name=None,
                 engineer_id=None,
                 payment_money=None,
                 remarks=None,
                 payment_start_day=None,
                 payment_end_day=None,
                 payment_per_month=None,
                 payment_rule=None,
                 payment_bottom_base_hour=None,
                 payment_top_base_hour=None,
                 payment_free_base_hour=None,
                 payment_per_hour=None,
                 payment_per_bottom_hour=None,
                 payment_per_top_hour=None,
                 payment_fraction=None,
                 payment_fraction_calculation1=None,
                 payment_fraction_calculation2=None,
                 bp_order_no=None,
                 client_order_no_for_bp=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(ProjectDetail, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_id = project_id
        self.detail_type = detail_type
        self.work_name = work_name
        self.engineer_id = engineer_id
        self.payment_money = payment_money
        self.remarks = remarks
        self.payment_start_day = payment_start_day
        self.payment_end_day = payment_end_day
        self.payment_per_month = payment_per_month
        self.payment_rule = payment_rule
        self.payment_bottom_base_hour = payment_bottom_base_hour
        self.payment_top_base_hour = payment_top_base_hour
        self.payment_free_base_hour = payment_free_base_hour
        self.payment_per_hour = payment_per_hour
        self.payment_per_bottom_hour = payment_per_bottom_hour
        self.payment_per_top_hour = payment_per_top_hour
        self.payment_fraction = payment_fraction
        self.payment_fraction_calculation1 = payment_fraction_calculation1
        self.payment_fraction_calculation2 = payment_fraction_calculation2
        self.bp_order_no = bp_order_no
        self.client_order_no_for_bp = client_order_no_for_bp

    def __repr__(self):
        return "<ProjectDetails:" + \
                "'id='{}".format(self.id) + \
                "', project='{}".format(self.project) + \
                "', detail_type='{}".format(self.detail_type) + \
                "', work_name='{}".format(self.work_name) + \
                "', engineer='{}".format(self.engineer) + \
                "', payment_money='{}".format(self.payment_money) + \
                "', remarks='{}".format(self.remarks) + \
                "', payment_start_day='{}".format(self.payment_start_day) + \
                "', payment_end_day='{}".format(self.payment_end_day) + \
                "', payment_per_month='{}".format(self.payment_per_month) + \
                "', payment_rule='{}".format(self.payment_rule) + \
                "', payment_bottom_base_hour='{}".format(self.payment_bottom_base_hour) + \
                "', payment_top_base_hour='{}".format(self.payment_top_base_hour) + \
                "', payment_free_base_hour='{}".format(self.payment_free_base_hour) + \
                "', payment_per_hour='{}".format(self.payment_per_hour) + \
                "', payment_per_bottom_hour='{}".format(self.payment_per_bottom_hour) + \
                "', payment_per_top_hour='{}".format(self.payment_per_top_hour) + \
                "', payment_fraction='{}".format(self.payment_fraction) + \
                "', payment_fraction_calculation1='{}".format(self.payment_fraction_calculation1) + \
                "', payment_fraction_calculation2='{}".format(self.payment_fraction_calculation2) + \
                "', bp_order_no='{}".format(self.bp_order_no) + \
                "', client_order_no_for_bp='{}".format(self.client_order_no_for_bp) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

    def is_engineer(self):
        return self.detail_type == DetailType.engineer

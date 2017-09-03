from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.sqlalchemy.types import EnumType


class ProjectResult(BaseModel, db.Model):
    __tablename__ = 'project_results'
    PER_PAGE = 10

    project_detail_id = Column(Integer, ForeignKey("project_details.id"), nullable=False)
    result_month = Column(Date)
    work_time = Column(DECIMAL(6, 2))
    billing_transportation = Column(Integer)
    billing_adjustments = Column(Integer)
    billing_confirmation_number = Column(String(128))
    billing_confirmation_money = Column(Integer)
    payment_transportation = Column(Integer)
    payment_adjustments = Column(Integer)
    payment_confirmation_money = Column(Integer)
    remarks = Column(String(1024))
    billing_receipted_date = Column(Date)
    payment_expected_date = Column(Date)
    payment_flag = Column(EnumType(enum_class=InputFlag), nullable=False, default=0)

    project_detail = relationship("ProjectDetail", lazy='joined')

    def __init__(self,
                 project_detail_id=None,
                 result_month=None,
                 work_time=None,
                 billing_transportation=None,
                 billing_adjustments=None,
                 billing_confirmation_number=None,
                 billing_confirmation_money=None,
                 payment_transportation=None,
                 payment_adjustments=None,
                 payment_confirmation_money=None,
                 remarks=None,
                 billing_receipted_date=None,
                 payment_expected_date=None,
                 payment_flag=InputFlag.yet,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(ProjectResult, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_detail_id = project_detail_id
        self.result_month = result_month
        self.work_time = work_time
        self.billing_transportation = billing_transportation
        self.billing_adjustments = billing_adjustments
        self.billing_confirmation_number = billing_confirmation_number
        self.billing_confirmation_money = billing_confirmation_money
        self.payment_transportation = payment_transportation
        self.payment_adjustments = payment_adjustments
        self.payment_confirmation_money = payment_confirmation_money
        self.remarks = remarks
        self.billing_receipted_date = billing_receipted_date
        self.payment_expected_date = payment_expected_date
        self.payment_flag = payment_flag

    def is_result_input(self):
        return (self.work_time or 0) > 0

    # 指定した月の支払い税率を取得
    def tax_of_payment_confirmation_money(self, engineer_history):
        if engineer_history:
            return (self.payment_confirmation_money or 0) * engineer_history.payment_tax.rate
        else:
            return 0

    def __repr__(self):
        return "<ProjectResult:" + \
                "'id='{}".format(self.id) + \
                "', project_detail_id='{}".format(self.project_detail_id) + \
                "', result_month='{}".format(self.result_month) + \
                "', work_time='{}".format(self.work_time) + \
                "', billing_transportation='{}".format(self.billing_transportation) + \
                "', billing_adjustments='{}".format(self.billing_adjustments) + \
                "', billing_confirmation_number='{}".format(self.billing_confirmation_number) + \
                "', billing_confirmation_money='{}".format(self.billing_confirmation_money) + \
                "', payment_transportation='{}".format(self.payment_transportation) + \
                "', payment_adjustments='{}".format(self.payment_adjustments) + \
                "', payment_confirmation_money='{}".format(self.payment_confirmation_money) + \
                "', remarks='{}".format(self.remarks) + \
                "', billing_receipted_date='{}".format(self.billing_receipted_date) + \
                "', payment_expected_date='{}".format(self.payment_expected_date) + \
                "', payment_flag='{}".format(self.payment_flag) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

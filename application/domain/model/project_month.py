from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.immutables.input_flag import InputFlag
from application.domain.model.sqlalchemy.types import EnumType


class ProjectMonth(BaseModel, db.Model):
    __tablename__ = 'project_months'

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project_month = Column(Date, nullable=False)
    billing_input_flag = Column(EnumType(enum_class=InputFlag), nullable=False, default=0)
    deposit_input_flag = Column(EnumType(enum_class=InputFlag), nullable=False, default=0)
    deposit_date = Column(Date)
    billing_estimated_money = Column(Integer)
    billing_confirmation_money = Column(Integer)
    billing_transportation = Column(Integer)
    remarks = Column(String(1024))
    client_billing_no = Column(String(64), unique=True)

    project = relationship("Project", lazy='joined')

    def __init__(self,
                 project_id=None,
                 project_month=None,
                 billing_input_flag=InputFlag.yet,
                 deposit_input_flag=InputFlag.yet,
                 deposit_date=None,
                 billing_estimated_money=None,
                 billing_confirmation_money=None,
                 billing_transportation=None,
                 remarks=None,
                 client_billing_no=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(ProjectMonth, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_id = project_id
        self.project_month = project_month
        self.billing_input_flag = billing_input_flag
        self.deposit_input_flag = deposit_input_flag
        self.deposit_date = deposit_date
        self.billing_estimated_money = billing_estimated_money
        self.billing_confirmation_money = billing_confirmation_money
        self.billing_transportation = billing_transportation
        self.remarks = remarks
        self.client_billing_no = client_billing_no

    @staticmethod
    def _get_fiscal_year(date_):
        if int(date_.strftime('%m')) >= 10:
            return int(date_.strftime('%y')) + 1
        else:
            return int(date_.strftime('%y'))

    def tax_of_billing_confirmation_money(self):
        return self.billing_confirmation_money * self.project.client_company.billing_tax.rate

    def has_billing(self):
        return (self.billing_estimated_money or 0) > 0 or (self.billing_confirmation_money or 0) > 0

    def is_month_to_billing(self):
        return not self.client_billing_no and (self.billing_confirmation_money or 0) > 0

    def get_fiscal_year(self):
        return self._get_fiscal_year(self.project_month)

    def __repr__(self):
        return "<ProjectMonth:" + \
                "'id='{}".format(self.id) + \
                "', project_id='{}".format(self.project_id) + \
                "', project_month='{}".format(self.project_month) + \
                "', billing_input_flag='{}".format(self.billing_input_flag) + \
                "', deposit_input_flag='{}".format(self.deposit_input_flag) + \
                "', deposit_date='{}".format(self.deposit_date) + \
                "', billing_estimated_money='{}".format(self.billing_estimated_money) + \
                "', billing_confirmation_money='{}".format(self.billing_confirmation_money) + \
                "', billing_transportation='{}".format(self.billing_transportation) + \
                "', remarks='{}".format(self.remarks) + \
                "', client_billing_no='{}".format(self.client_billing_no) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

from sqlalchemy import Column, Integer, String, Date, ForeignKey

from application import db
from application.const import BILLING_STATUS
from application.domain.model.base_model import BaseModel


class Billing(BaseModel, db.Model):
    __tablename__ = 'billings'
    PER_PAGE = 10

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    billing_month = Column(Date, nullable=False)
    billing_amount = Column(Integer)
    billing_adjustment_amount = Column(Integer)
    tax = Column(Integer)
    carfare = Column(Integer)
    scheduled_billing_date = Column(Date)
    billing_date = Column(Date)
    bill_output_date = Column(Date)
    scheduled_payment_date = Column(Date)
    payment_date = Column(Date)
    status = Column(Integer)
    remarks = Column(String(1024))

    def __init__(self,
                 project_id=None,
                 billing_month=None,
                 billing_amount=None,
                 billing_adjustment_amount=None,
                 tax=None,
                 carfare=None,
                 scheduled_billing_date=None,
                 billing_date=None,
                 bill_output_date=None,
                 scheduled_payment_date=None,
                 payment_date=None,
                 status=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Billing, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_id = project_id
        self.billing_month = billing_month
        self.billing_amount = billing_amount
        self.billing_adjustment_amount = billing_adjustment_amount
        self.tax = tax
        self.carfare = carfare
        self.scheduled_billing_date = scheduled_billing_date
        self.billing_date = billing_date
        self.bill_output_date = bill_output_date
        self.scheduled_payment_date = scheduled_payment_date
        self.payment_date = payment_date
        self.status = status
        self.remarks = remarks

    def get_status_name(self):
        if self.status is None:
            return None
        else:
            return BILLING_STATUS[str(self.status)]

    def __repr__(self):
        return "<Billing:" + \
                "'id='{}".format(self.id) + \
                "', project_id='{}".format(self.project_id) + \
                "', billing_month='{}".format(self.billing_month) + \
                "', billing_amount='{}".format(self.billing_amount) + \
                "', billing_adjustment_amount='{}".format(self.billing_adjustment_amount) + \
                "', tax='{}".format(self.tax) + \
                "', carfare='{}".format(self.carfare) + \
                "', scheduled_billing_date='{}".format(self.scheduled_billing_date) + \
                "', billing_date='{}".format(self.billing_date) + \
                "', bill_output_date='{}".format(self.bill_output_date) + \
                "', scheduled_payment_date='{}".format(self.scheduled_payment_date) + \
                "', payment_date='{}".format(self.payment_date) + \
                "', status='{}".format(self.status) + \
                "', remarks='{}".format(self.remarks) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

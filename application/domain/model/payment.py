from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.engineer import Engineer


class Payment(BaseModel, db.Model):
    __tablename__ = 'payments'
    PER_PAGE = 10

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    payment_month = Column(Date, nullable=False)
    engineer_id = Column(Integer, ForeignKey("engineers.id"))
    payment_amount = Column(Integer)
    payment_adjustment_amount = Column(Integer)
    tax = Column(Integer)
    carfare = Column(Integer)
    scheduled_payment_date = Column(Date)
    payment_date = Column(Date)
    status = Column(Integer)
    remarks = Column(String(1024))

    engineer = relationship(Engineer, lazy='joined')

    def __init__(self,
                 project_id=None,
                 payment_month=None,
                 engineer_id=None,
                 payment_amount=None,
                 payment_adjustment_amount=None,
                 tax=None,
                 carfare=None,
                 scheduled_payment_date=None,
                 payment_date=None,
                 status=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Payment, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_id = project_id
        self.payment_month = payment_month
        self.engineer_id = engineer_id
        self.payment_amount = payment_amount
        self.payment_adjustment_amount = payment_adjustment_amount
        self.tax = tax
        self.carfare = carfare
        self.scheduled_payment_date = scheduled_payment_date
        self.payment_date = payment_date
        self.status = status
        self.remarks = remarks

    def __repr__(self):
        return "<Payment:" + \
                "'id='{}".format(self.id) + \
                "', project_id='{}".format(self.project_id) + \
                "', payment_month='{}".format(self.payment_month) + \
                "', engineer_id='{}".format(self.engineer_id) + \
                "', payment_amount='{}".format(self.payment_amount) + \
                "', payment_adjustment_amount='{}".format(self.payment_adjustment_amount) + \
                "', tax='{}".format(self.tax) + \
                "', carfare='{}".format(self.carfare) + \
                "', scheduled_payment_date='{}".format(self.scheduled_payment_date) + \
                "', payment_date='{}".format(self.payment_date) + \
                "', status='{}".format(self.status) + \
                "', remarks='{}".format(self.remarks) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

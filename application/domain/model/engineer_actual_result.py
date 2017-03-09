from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.engineer import Engineer


class EngineerActualResult(BaseModel, db.Model):
    __tablename__ = 'engineer_actual_results'
    PER_PAGE = 10

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    result_month = Column(Date, nullable=False)
    seq_no = Column(Integer, nullable=False)
    engineer_id = Column(Integer, ForeignKey("engineers.id"))
    fixed_flg = Column(String(1), nullable=False)
    working_hours = Column(DECIMAL(5, 2))
    adjustment_hours = Column(DECIMAL(5, 2))
    billing_amount = Column(Integer)
    billing_adjustment_amount = Column(Integer)
    payment_amount = Column(Integer)
    payment_adjustment_amount = Column(Integer)
    carfare = Column(Integer)
    remarks = Column(String(1024))

    engineer = relationship(Engineer, lazy='joined')

    def __init__(self,
                 project_id=None,
                 result_month=None,
                 seq_no=None,
                 engineer_id=None,
                 fixed_flg='0',
                 working_hours=None,
                 adjustment_hours=None,
                 billing_amount=None,
                 billing_adjustment_amount=None,
                 payment_amount=None,
                 payment_adjustment_amount=None,
                 carfare=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(EngineerActualResult, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_id = project_id
        self.result_month = result_month
        self.seq_no = seq_no
        self.engineer_id = engineer_id
        self.fixed_flg = fixed_flg
        self.working_hours = working_hours
        self.adjustment_hours = adjustment_hours
        self.billing_amount = billing_amount
        self.billing_adjustment_amount = billing_adjustment_amount
        self.payment_amount = payment_amount
        self.payment_adjustment_amount = payment_adjustment_amount
        self.carfare = carfare
        self.remarks = remarks

    def __repr__(self):
        return "<EngineerActualResult:" + \
                "'id='{}".format(self.id) + \
                "', project_id='{}".format(self.project_id) + \
                "', result_month='{}".format(self.result_month) + \
                "', seq_no='{}".format(self.seq_no) + \
                "', engineer_id='{}".format(self.engineer_id) + \
                "', fixed_flg='{}".format(self.fixed_flg) + \
                "', working_hours='{}".format(self.working_hours) + \
                "', adjustment_hours='{}".format(self.adjustment_hours) + \
                "', billing_amount='{}".format(self.billing_amount) + \
                "', billing_adjustment_amount='{}".format(self.billing_adjustment_amount) + \
                "', payment_amount='{}".format(self.payment_amount) + \
                "', payment_adjustment_amount='{}".format(self.payment_adjustment_amount) + \
                "', carfare='{}".format(self.carfare) + \
                "', remarks='{}".format(self.remarks) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

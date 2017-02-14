from sqlalchemy import Column, Integer, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.engineer import Engineer


class AssignedMember(BaseModel, db.Model):
    __tablename__ = 'assigned_members'
    PER_PAGE = 10

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    seq_no = Column(Integer, nullable=False)
    engineer_id = Column(Integer, ForeignKey("engineers.id"))
    sales_unit_price = Column(Integer, nullable=False)
    payment_unit_price = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    engineer = relationship(Engineer, lazy='joined')

    def __init__(self,
                 project_id=None,
                 seq_no=None,
                 engineer_id=None,
                 sales_unit_price=None,
                 payment_unit_price=None,
                 start_date=None,
                 end_date=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(AssignedMember, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_id = project_id
        self.seq_no = seq_no
        self.engineer_id = engineer_id
        self.sales_unit_price = sales_unit_price
        self.payment_unit_price = payment_unit_price
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return "<AssignedMember:" + \
                "'id='{}".format(self.id) + \
                "', seq_no='{}".format(self.seq_no) + \
                "', engineer='{}".format(self.engineer) + \
                "', sales_unit_price='{}".format(self.sales_unit_price) + \
                "', payment_unit_price='{}".format(self.payment_unit_price) + \
                "', start_date='{}".format(self.start_date) + \
                "', end_date='{}".format(self.end_date) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

    def clone(self):
        arguments = dict()
        copy = AssignedMember()
        for name, column in self.__mapper__.columns.items():
            if not (column.primary_key or column.unique):
                arguments[name] = getattr(self, name)
        return copy.__class__(**arguments)

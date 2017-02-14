from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.company import Company


class OrderRemarks(BaseModel, db.Model):
    __tablename__ = 'order_remarks'
    PER_PAGE = 10

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    order_no = Column(String(64), nullable=False)
    order_amount = Column(Integer)
    contents = Column(String(1024))
    responsible_person = Column(String(128))
    subcontractor = Column(String(128))
    scope = Column(String(1024))
    work_place = Column(String(1024))
    delivery_place = Column(String(1024))
    deliverables = Column(String(1024))
    inspection_date = Column(Date)
    payment_terms = Column(String(1024))
    billing_company_id = Column(Integer, ForeignKey("companies.id"))
    remarks = Column(String(1024))

    billing_company = relationship(Company, lazy='joined')

    def __init__(self,
                 project_id=None,
                 order_no=None,
                 order_amount=None,
                 contents=None,
                 responsible_person=None,
                 subcontractor=None,
                 scope=None,
                 work_place=None,
                 delivery_place=None,
                 deliverables=None,
                 inspection_date=None,
                 payment_terms=None,
                 billing_company_id=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(OrderRemarks, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_id = project_id
        self.order_no = order_no
        self.order_amount = order_amount
        self.contents = contents
        self.responsible_person = responsible_person
        self.subcontractor = subcontractor
        self.scope = scope
        self.work_place = work_place
        self.delivery_place = delivery_place
        self.deliverables = deliverables
        self.inspection_date = inspection_date
        self.payment_terms = payment_terms
        self.billing_company_id = billing_company_id
        self.remarks = remarks

    def __repr__(self):
        return "<OrderRemarks:" + \
                "'id='{}".format(self.id) + \
                "', project_id'{}".format(self.project_id) + \
                "', order_no'{}".format(self.order_no) + \
                "', order_amount'{}".format(self.order_amount) + \
                "', contents'{}".format(self.contents) + \
                "', responsible_person'{}".format(self.responsible_person) + \
                "', subcontractor'{}".format(self.subcontractor) + \
                "', scope'{}".format(self.scope) + \
                "', work_place'{}".format(self.work_place) + \
                "', delivery_place'{}".format(self.delivery_place) + \
                "', deliverables'{}".format(self.deliverables) + \
                "', inspection_date'{}".format(self.inspection_date) + \
                "', payment_terms'{}".format(self.payment_terms) + \
                "', billing_company_id'{}".format(self.billing_company_id) + \
                "', remarks'{}".format(self.remarks) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

    def clone(self):
        arguments = dict()
        copy = OrderRemarks()
        for name, column in self.__mapper__.columns.items():
            if not (column.primary_key or column.unique):
                arguments[name] = getattr(self, name)
        return copy.__class__(**arguments)

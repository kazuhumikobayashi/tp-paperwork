from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel


class ProjectBilling(BaseModel, db.Model):
    __tablename__ = 'project_billings'

    project_detail_id = Column(Integer, ForeignKey("project_details.id"), nullable=False)
    billing_month = Column(Date, nullable=False)
    billing_content = Column(String(128))
    billing_amount = Column(String(128))
    billing_confirmation_money = Column(String(128))
    remarks = Column(String(128))

    project_detail = relationship("ProjectDetail", lazy='joined')

    def __init__(self,
                 project_detail_id=None,
                 billing_month=None,
                 billing_content=None,
                 billing_amount=None,
                 billing_confirmation_money=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(ProjectBilling, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_detail_id = project_detail_id
        self.billing_month = billing_month
        self.billing_content = billing_content
        self.billing_amount = billing_amount
        self.billing_confirmation_money = billing_confirmation_money
        self.remarks = remarks

    def __repr__(self):
        return "<ProjectBilling:" + \
                "'id='{}".format(self.id) + \
                "', project_detail_id='{}".format(self.project_detail_id) + \
                "', billing_month='{}".format(self.billing_month) + \
                "', billing_content='{}".format(self.billing_content) + \
                "', billing_amount='{}".format(self.billing_amount) + \
                "', billing_confirmation_money='{}".format(self.billing_confirmation_money) + \
                "', remarks='{}".format(self.remarks) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

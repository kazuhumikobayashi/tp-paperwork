from sqlalchemy import Column, String

from application import db
from application.domain.model.base_model import BaseModel


class Department(BaseModel, db.Model):
    __tablename__ = 'departments'
    PER_PAGE = 10

    group_name = Column(String(128), nullable=False)
    department_name = Column(String(128), nullable=False)

    def __init__(self,
                 group_name=None,
                 department_name=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Department, self).__init__(created_at, created_user, updated_at, updated_user)
        self.group_name = group_name
        self.department_name = department_name

    def __repr__(self):
        return "<Department:" + \
                "'id='{}".format(self.id) + \
                "', group_name='{}".format(self.group_name) + \
                "', department_name='{}".format(self.department_name) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

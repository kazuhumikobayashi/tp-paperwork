from sqlalchemy import Column, String

from application import db
from application.domain.model.base_model import BaseModel


class Skill(BaseModel, db.Model):
    __tablename__ = 'skills'
    PER_PAGE = 10

    skill_name = Column(String(32), nullable=False)

    def __init__(self,
                 skill_name=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Skill, self).__init__(created_at, created_user, updated_at, updated_user)
        self.skill_name = skill_name

    def __repr__(self):
        return "<Skill:" + \
                "'id='{}".format(self.id) + \
                "', skill_name='{}".format(self.skill_name) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

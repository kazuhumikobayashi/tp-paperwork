from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.skill import Skill


class EngineerSkill(BaseModel, db.Model):
    __tablename__ = 'engineer_skills'
    PER_PAGE = 10

    engineer_id = Column(Integer, ForeignKey("engineers.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    skill = relationship(Skill, lazy='joined')

    def __init__(self,
                 engineer_id=None,
                 skill_id=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(EngineerSkill, self).__init__(created_at, created_user, updated_at, updated_user)
        self.engineer_id = engineer_id
        self.skill_id = skill_id

    def __repr__(self):
        return "<EngineerSkill:" + \
                "'id='{}".format(self.id) + \
                "', engineer_id='{}".format(self.engineer_id) + \
                "', skill_id='{}".format(self.skill_id) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

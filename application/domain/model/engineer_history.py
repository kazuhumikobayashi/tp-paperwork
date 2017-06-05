from sqlalchemy import Column, Integer, Date, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.immutables.expression import Expression
from application.domain.model.immutables.round import Round
from application.domain.model.immutables.rule import Rule
from application.domain.model.sqlalchemy.types import EnumType


class EngineerHistory(BaseModel, db.Model):
    __tablename__ = 'engineer_histories'
    PER_PAGE = 10

    engineer_id = Column(Integer, ForeignKey("engineers.id"))
    receipt_start_day = Column(Date, nullable=False)
    receipt_end_day = Column(Date, nullable=False)
    receipt_per_month = Column(Integer, nullable=False)
    receipt_rule = Column(EnumType(enum_class=Rule), nullable=False)
    receipt_bottom_base_hour = Column(Integer)
    receipt_top_base_hour = Column(Integer)
    receipt_free_base_hour = Column(String(128))
    receipt_per_hour = Column(String(128))
    receipt_per_bottom_hour = Column(Integer)
    receipt_per_top_hour = Column(Integer)
    receipt_fraction = Column(Integer)
    receipt_fraction_calculation1 = Column(EnumType(enum_class=Expression))
    receipt_fraction_calculation2 = Column(EnumType(enum_class=Round))
    receipt_condition = Column(String(1024))
    remarks = Column(String(1024))

    engineer = relationship("Engineer", lazy='joined')

    def __init__(self,
                 engineer_id=None,
                 receipt_start_day=None,
                 receipt_end_day=None,
                 receipt_per_month=None,
                 receipt_rule=None,
                 receipt_bottom_base_hour=None,
                 receipt_top_base_hour=None,
                 receipt_free_base_hour=None,
                 receipt_per_hour=None,
                 receipt_per_bottom_hour=None,
                 receipt_per_top_hour=None,
                 receipt_fraction=None,
                 receipt_fraction_calculation1=None,
                 receipt_fraction_calculation2=None,
                 receipt_condition=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(EngineerHistory, self).__init__(created_at, created_user, updated_at, updated_user)
        self.engineer_id = engineer_id
        self.receipt_start_day = receipt_start_day
        self.receipt_end_day = receipt_end_day
        self.receipt_per_month = receipt_per_month
        self.receipt_rule = receipt_rule
        self.receipt_bottom_base_hour = receipt_bottom_base_hour
        self.receipt_top_base_hour = receipt_top_base_hour
        self.receipt_free_base_hour = receipt_free_base_hour
        self.receipt_per_hour = receipt_per_hour
        self.receipt_per_bottom_hour = receipt_per_bottom_hour
        self.receipt_per_top_hour = receipt_per_top_hour
        self.receipt_fraction = receipt_fraction
        self.receipt_fraction_calculation1 = receipt_fraction_calculation1
        self.receipt_fraction_calculation2 = receipt_fraction_calculation2
        self.receipt_condition = receipt_condition
        self.remarks = remarks

    def __repr__(self):
        return "<EngineerHistory:" + \
                "'id='{}".format(self.id) + \
                "', engineer='{}".format(self.engineer) + \
                "', receipt_start_day='{}".format(self.receipt_start_day) + \
                "', receipt_end_day='{}".format(self.receipt_end_day) + \
                "', receipt_per_month='{}".format(self.receipt_per_month) + \
                "', receipt_rule='{}".format(self.receipt_rule) + \
                "', receipt_bottom_base_hour='{}".format(self.receipt_bottom_base_hour) + \
                "', receipt_top_base_hour='{}".format(self.receipt_top_base_hour) + \
                "', receipt_free_base_hour='{}".format(self.receipt_free_base_hour) + \
                "', receipt_per_hour='{}".format(self.receipt_per_hour) + \
                "', receipt_per_bottom_hour='{}".format(self.receipt_per_bottom_hour) + \
                "', receipt_per_top_hour='{}".format(self.receipt_per_top_hour) + \
                "', receipt_fraction='{}".format(self.receipt_fraction) + \
                "', receipt_fraction_calculation1='{}".format(self.receipt_fraction_calculation1) + \
                "', receipt_fraction_calculation2='{}".format(self.receipt_fraction_calculation2) + \
                "', receipt_condition='{}".format(self.receipt_condition) + \
                "', remarks='{}".format(self.remarks) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

    # 履歴を切る際にengineer情報を紐づけたまま新規履歴を作成して返すメソッド
    def create_new_history(self):
        # engineerをhistoryに紐づけた状態で返す
        engineer_history = EngineerHistory()
        engineer_history.engineer = self.engineer
        return engineer_history

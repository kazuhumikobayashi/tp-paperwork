from sqlalchemy import Column, Integer, Date, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.immutables.fraction import Fraction
from application.domain.model.immutables.round import Round
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.site import Site
from application.domain.model.immutables.tax import Tax
from application.domain.model.sqlalchemy.types import EnumType


class EngineerHistory(BaseModel, db.Model):
    __tablename__ = 'engineer_histories'
    PER_PAGE = 10

    engineer_id = Column(Integer, ForeignKey("engineers.id"))
    payment_start_day = Column(Date, nullable=False)
    payment_end_day = Column(Date, nullable=False)
    payment_site = Column(EnumType(enum_class=Site))
    payment_tax = Column(EnumType(enum_class=Tax))
    payment_per_month = Column(Integer, nullable=False)
    payment_rule = Column(EnumType(enum_class=Rule), nullable=False)
    payment_bottom_base_hour = Column(Integer)
    payment_top_base_hour = Column(Integer)
    payment_free_base_hour = Column(String(128))
    payment_per_hour = Column(String(128))
    payment_per_bottom_hour = Column(Integer)
    payment_per_top_hour = Column(Integer)
    payment_fraction = Column(EnumType(enum_class=Fraction))
    payment_fraction_rule = Column(EnumType(enum_class=Round))
    payment_condition = Column(String(1024))
    remarks = Column(String(1024))

    engineer = relationship("Engineer", lazy='joined')

    def __init__(self,
                 engineer_id=None,
                 payment_start_day=None,
                 payment_end_day=None,
                 payment_per_month=None,
                 payment_rule=None,
                 payment_site=None,
                 payment_tax=None,
                 payment_bottom_base_hour=None,
                 payment_top_base_hour=None,
                 payment_free_base_hour=None,
                 payment_per_hour=None,
                 payment_per_bottom_hour=None,
                 payment_per_top_hour=None,
                 payment_fraction=None,
                 payment_fraction_rule=None,
                 payment_condition=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(EngineerHistory, self).__init__(created_at, created_user, updated_at, updated_user)
        self.engineer_id = engineer_id
        self.payment_start_day = payment_start_day
        self.payment_end_day = payment_end_day
        self.payment_site = payment_site
        self.payment_tax = payment_tax
        self.payment_per_month = payment_per_month
        self.payment_rule = payment_rule
        self.payment_bottom_base_hour = payment_bottom_base_hour
        self.payment_top_base_hour = payment_top_base_hour
        self.payment_free_base_hour = payment_free_base_hour
        self.payment_per_hour = payment_per_hour
        self.payment_per_bottom_hour = payment_per_bottom_hour
        self.payment_per_top_hour = payment_per_top_hour
        self.payment_fraction = payment_fraction
        self.payment_fraction_rule = payment_fraction_rule
        self.payment_condition = payment_condition
        self.remarks = remarks

    # 履歴を切る際にengineer情報を紐づけたまま新規履歴を作成して返すメソッド
    def create_new_history(self):
        # engineerをhistoryに紐づけた状態で返す
        engineer_history = EngineerHistory()
        engineer_history.engineer = self.engineer
        return engineer_history

    def __repr__(self):
        return "<EngineerHistory:" + \
                "'id='{}".format(self.id) + \
                "', engineer='{}".format(self.engineer) + \
                "', payment_start_day='{}".format(self.payment_start_day) + \
                "', payment_end_day='{}".format(self.payment_end_day) + \
                "', payment_site='{}".format(self.payment_site) + \
                "', payment_tax='{}".format(self.payment_tax) + \
                "', payment_per_month='{}".format(self.payment_per_month) + \
                "', payment_rule='{}".format(self.payment_rule) + \
                "', payment_bottom_base_hour='{}".format(self.payment_bottom_base_hour) + \
                "', payment_top_base_hour='{}".format(self.payment_top_base_hour) + \
                "', payment_free_base_hour='{}".format(self.payment_free_base_hour) + \
                "', payment_per_hour='{}".format(self.payment_per_hour) + \
                "', payment_per_bottom_hour='{}".format(self.payment_per_bottom_hour) + \
                "', payment_per_top_hour='{}".format(self.payment_per_top_hour) + \
                "', payment_fraction='{}".format(self.payment_fraction) + \
                "', payment_fraction_rule='{}".format(self.payment_fraction_rule) + \
                "', payment_condition='{}".format(self.payment_condition) + \
                "', remarks='{}".format(self.remarks) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

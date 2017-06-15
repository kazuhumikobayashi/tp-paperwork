from datetime import date

from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.holiday_flag import HolidayFlag
from application.domain.model.immutables.rule import Rule
from application.domain.model.project_billing import ProjectBilling
from application.domain.model.project_result import ProjectResult
from application.domain.model.sqlalchemy.types import EnumType
from application.service.calculator import Calculator


class ProjectDetail(BaseModel, db.Model):
    __tablename__ = 'project_details'
    PER_PAGE = 10

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    detail_type = Column(EnumType(enum_class=DetailType), nullable=False)
    work_name = Column(String(128))
    engineer_id = Column(Integer, ForeignKey("engineers.id"))
    _billing_money = Column('billing_money', Integer)
    remarks = Column(String(1024))
    billing_start_day = Column(Date)
    billing_end_day = Column(Date)
    billing_per_month = Column(Integer)
    billing_rule = Column(EnumType(enum_class=Rule))
    billing_bottom_base_hour = Column(Integer)
    billing_top_base_hour = Column(Integer)
    billing_free_base_hour = Column(String(128))
    billing_per_hour = Column(String(128))
    billing_per_bottom_hour = Column(Integer)
    billing_per_top_hour = Column(Integer)
    billing_fraction = Column(Integer)
    billing_fraction_calculation1 = Column(Integer)
    billing_fraction_calculation2 = Column(Integer)
    bp_order_no = Column(String(128))
    client_order_no_for_bp = Column(String(128))

    engineer = relationship("Engineer", lazy='joined')
    project = relationship("Project", lazy='joined')
    project_billings = relationship(ProjectBilling, cascade='all, delete-orphan')
    project_results = relationship(ProjectResult, cascade='all, delete-orphan')

    @hybrid_property
    def billing_money(self):
        return self._billing_money

    @billing_money.setter
    def billing_money(self, value):
        self.project.estimated_total_amount = (self.project.estimated_total_amount or 0)\
                                              + (value or 0) \
                                              - (self._billing_money or 0)
        self._billing_money = value

    def __init__(self,
                 project_id=None,
                 detail_type=None,
                 work_name=None,
                 engineer_id=None,
                 billing_money=None,
                 remarks=None,
                 billing_start_day=None,
                 billing_end_day=None,
                 billing_per_month=None,
                 billing_rule=None,
                 billing_bottom_base_hour=None,
                 billing_top_base_hour=None,
                 billing_free_base_hour=None,
                 billing_per_hour=None,
                 billing_per_bottom_hour=None,
                 billing_per_top_hour=None,
                 billing_fraction=None,
                 billing_fraction_calculation1=None,
                 billing_fraction_calculation2=None,
                 bp_order_no=None,
                 client_order_no_for_bp=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(ProjectDetail, self).__init__(created_at, created_user, updated_at, updated_user)
        self.project_id = project_id
        self.detail_type = detail_type
        self.work_name = work_name
        self.engineer_id = engineer_id
        self._billing_money = billing_money
        self.remarks = remarks
        self.billing_start_day = billing_start_day
        self.billing_end_day = billing_end_day
        self.billing_per_month = billing_per_month
        self.billing_rule = billing_rule
        self.billing_bottom_base_hour = billing_bottom_base_hour
        self.billing_top_base_hour = billing_top_base_hour
        self.billing_free_base_hour = billing_free_base_hour
        self.billing_per_hour = billing_per_hour
        self.billing_per_bottom_hour = billing_per_bottom_hour
        self.billing_per_top_hour = billing_per_top_hour
        self.billing_fraction = billing_fraction
        self.billing_fraction_calculation1 = billing_fraction_calculation1
        self.billing_fraction_calculation2 = billing_fraction_calculation2
        self.bp_order_no = bp_order_no
        self.client_order_no_for_bp = client_order_no_for_bp

    def is_engineer(self):
        return self.detail_type == DetailType.engineer

    # 支払予定日を計算するメソッド
    def get_payment_date(self, date):
        # 支払予定日はBPのみ記述
        if self.is_engineer() and self.engineer.is_bp():
            payment_site = self.engineer.company.payment_site

            # 支払いの場合、末日は前倒し、その他後ろ倒し
            if payment_site.is_last_day():
                bank_holiday_flag = HolidayFlag.before
            else:
                bank_holiday_flag = HolidayFlag.after

            # 入金サイトから支払日を選定
            deposit_date = Calculator.calculate_deposit_date_from_site(date, payment_site.value)

            # 土日の場合、前倒し・後ろ倒しの日付に変更。
            deposit_date = Calculator.to_weekday_if_on_weekend(deposit_date, bank_holiday_flag)

            # 祝日の場合、前倒し・後ろ倒しの日付に変更。
            deposit_date = Calculator.to_weekday_if_on_holiday(deposit_date, bank_holiday_flag)

            return deposit_date
        return None

    # 開始・終了日のそれぞれの年月をリストで返すメソッド
    def get_contract_month_list(self):
        contract_month_list = []
        i = 0
        start = self.billing_start_day
        while (date(start.year, start.month, 1) + relativedelta(months=i)) <= self.billing_end_day:
            contract_month_list.append(date(start.year, start.month, 1) + relativedelta(months=i))
            i += 1
        return contract_month_list

    # 作業の請求単価（ひと月当たりに請求する金額）を取得
    def get_payment_per_month_by_work(self):
        payment = self.billing_money / len(self.project.get_project_month_list())
        # TODO 端数計算処理実行
        return payment

    def __repr__(self):
        return "<ProjectDetails:" + \
                "'id='{}".format(self.id) + \
                "', project='{}".format(self.project) + \
                "', detail_type='{}".format(self.detail_type) + \
                "', work_name='{}".format(self.work_name) + \
                "', engineer='{}".format(self.engineer) + \
                "', billing_money='{}".format(self.billing_money) + \
                "', remarks='{}".format(self.remarks) + \
                "', billing_start_day='{}".format(self.billing_start_day) + \
                "', billing_end_day='{}".format(self.billing_end_day) + \
                "', billing_per_month='{}".format(self.billing_per_month) + \
                "', billing_rule='{}".format(self.billing_rule) + \
                "', billing_bottom_base_hour='{}".format(self.billing_bottom_base_hour) + \
                "', billing_top_base_hour='{}".format(self.billing_top_base_hour) + \
                "', billing_free_base_hour='{}".format(self.billing_free_base_hour) + \
                "', billing_per_hour='{}".format(self.billing_per_hour) + \
                "', billing_per_bottom_hour='{}".format(self.billing_per_bottom_hour) + \
                "', billing_per_top_hour='{}".format(self.billing_per_top_hour) + \
                "', billing_fraction='{}".format(self.billing_fraction) + \
                "', billing_fraction_calculation1='{}".format(self.billing_fraction_calculation1) + \
                "', billing_fraction_calculation2='{}".format(self.billing_fraction_calculation2) + \
                "', bp_order_no='{}".format(self.bp_order_no) + \
                "', client_order_no_for_bp='{}".format(self.client_order_no_for_bp) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

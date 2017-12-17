from datetime import date, datetime

from dateutil.tz import tz
from flask import session

from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.base_model import BaseModel
from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.fraction import Fraction
from application.domain.model.immutables.holiday_flag import HolidayFlag
from application.domain.model.immutables.round import Round
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
    billing_money = Column(Integer)
    remarks = Column(String(1024))
    _billing_start_day = Column('billing_start_day', Date)
    billing_end_day = Column(Date)
    billing_per_month = Column(Integer)
    billing_rule = Column(EnumType(enum_class=Rule))
    billing_bottom_base_hour = Column(Integer)
    billing_top_base_hour = Column(Integer)
    billing_free_base_hour = Column(String(128))
    billing_per_hour = Column(String(128))
    billing_per_bottom_hour = Column(Integer)
    billing_per_top_hour = Column(Integer)
    billing_fraction = Column(EnumType(enum_class=Fraction))
    billing_fraction_rule = Column(EnumType(enum_class=Round))
    bp_order_no = Column(String(128))
    client_order_no_for_bp = Column(String(128))

    engineer = relationship("Engineer", lazy='joined')
    project = relationship("Project", lazy='joined')
    project_billings = relationship(ProjectBilling, cascade='all, delete-orphan')
    project_results = relationship(ProjectResult, cascade='all, delete-orphan')

    _is_billing_start_day_change = False

    @hybrid_property
    def billing_start_day(self):
        return self._billing_start_day

    @billing_start_day.setter
    def billing_start_day(self, value):
        old = self._get_fiscal_year(self._billing_start_day)
        new = self._get_fiscal_year(value)

        if old != new:
            self._is_billing_start_day_change = True
        self._billing_start_day = value

    @property
    def is_billing_start_day_change(self):
        if not self.id:
            return True
        return self._is_billing_start_day_change

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
                 billing_fraction_rule=None,
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
        self.billing_money = billing_money
        self.remarks = remarks
        self._billing_start_day = billing_start_day
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
        self.billing_fraction_rule = billing_fraction_rule
        self.bp_order_no = bp_order_no
        self.client_order_no_for_bp = client_order_no_for_bp

    @staticmethod
    def _get_fiscal_year(date_):
        if not date_:
            return None
        if int(date_.strftime('%m')) >= 10:
            return int(date_.strftime('%y')) + 1
        else:
            return int(date_.strftime('%y'))

    def is_engineer(self):
        return self.detail_type == DetailType.engineer

    def has_payment(self):
        return self.is_engineer() and self.engineer.is_bp()

    def get_fiscal_year(self):
        return self._get_fiscal_year(self.billing_start_day)

    # 支払フラグが前倒しか後ろ倒しか判断
    def get_holiday_flag_if_payment(self):
        payment_site = self.get_payment_site()

        # 支払いの場合、末日は前倒し、その他後ろ倒し
        if payment_site.is_last_day():
            bank_holiday_flag = HolidayFlag.before
        else:
            bank_holiday_flag = HolidayFlag.after

        return bank_holiday_flag

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
        return payment

    # 月々の実績情報を作成
    def create_results(self):
        contract_dates = self.get_contract_month_list()
        for contract_date in contract_dates:
            jst = tz.gettz('Asia/Tokyo')
            now = datetime.now(jst)
            project_result = ProjectResult(
                                result_month=contract_date,
                                created_at=now,
                                created_user=session['user']['user_name'],
                                updated_at=now,
                                updated_user=session['user']['user_name'])
            if self.has_payment():
                calculator = Calculator(
                                contract_date,
                                self.get_payment_site(),
                                self.get_holiday_flag_if_payment())
                project_result.payment_expected_date = calculator.get_deposit_date()
            self.project_results.append(project_result)
        return self

    # 請求情報を作成
    def create_billings(self):
        if self.project.billing_timing == BillingTiming.billing_by_month:
            self.create_billing_by_month()
        else:
            self.create_billing_at_last()
        return self

    # 月々の請求情報を作成
    def create_billing_by_month(self):
        project_dates = self.project.get_project_month_list()
        for project_date in project_dates:
            jst = tz.gettz('Asia/Tokyo')
            now = datetime.now(jst)
            project_billing = ProjectBilling(
                                    billing_month=project_date,
                                    billing_content=self.work_name,
                                    billing_confirmation_money=self.get_payment_per_month_by_work(),
                                    created_at=now,
                                    created_user=session['user']['user_name'],
                                    updated_at=now,
                                    updated_user=session['user']['user_name'])
            self.project_billings.append(project_billing)
        return self

    # 最終月の請求情報を作成
    def create_billing_at_last(self):
        project_dates = self.project.get_project_month_list()
        jst = tz.gettz('Asia/Tokyo')
        now = datetime.now(jst)
        project_billing = ProjectBilling(
                                billing_month=max(project_dates),
                                billing_content=self.work_name,
                                billing_confirmation_money=self.billing_money,
                                created_at=now,
                                created_user=session['user']['user_name'],
                                updated_at=now,
                                updated_user=session['user']['user_name'])
        self.project_billings.append(project_billing)
        return self

    # 技術者履歴から支払いサイトを取得する。履歴が存在しない場合は会社から取得
    def get_payment_site(self):
        site = self.engineer.get_payment_site_by_date(self.project.start_date)
        return site or self.engineer.company.payment_site

    def __repr__(self):
        return "<ProjectDetails:" + \
                "'id='{}".format(self.id) + \
                "', project='{}".format(self.project) + \
                "', detail_type='{}".format(self.detail_type) + \
                "', work_name='{}".format(self.work_name) + \
                "', engineer_id='{}".format(self.engineer_id) + \
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
                "', billing_fraction_rule='{}".format(self.billing_fraction_rule) + \
                "', bp_order_no='{}".format(self.bp_order_no) + \
                "', client_order_no_for_bp='{}".format(self.client_order_no_for_bp) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

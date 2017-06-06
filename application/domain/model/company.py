from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.bank import Bank
from application.domain.model.base_model import BaseModel
from application.domain.model.company_client_flag import CompanyClientFlag
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.holiday_flag import HolidayFlag
from application.domain.model.immutables.site import Site
from application.domain.model.immutables.tax import Tax
from application.domain.model.sqlalchemy.types import EnumType


class Company(BaseModel, db.Model):
    __tablename__ = 'companies'
    PER_PAGE = 10

    company_name = Column(String(128), nullable=False)
    company_name_kana = Column(String(128))
    company_short_name = Column(String(128))
    contract_date = Column(Date)
    postal_code = Column(String(32))
    address = Column(String(1024))
    phone = Column(String(32))
    fax = Column(String(32))
    client_code = Column(String(128))
    bp_code = Column(String(128))
    billing_site = Column(EnumType(enum_class=Site))
    payment_site = Column(EnumType(enum_class=Site))
    billing_tax = Column(EnumType(enum_class=Tax))
    payment_tax = Column(EnumType(enum_class=Tax))
    bank_id = Column(Integer, ForeignKey("banks.id"))
    bank_holiday_flag = Column(EnumType(enum_class=HolidayFlag))
    remarks = Column(String(1024)) 
    print_name = Column(String(1024))

    bank = relationship(Bank, lazy='joined')
    company_client_flags = relationship(CompanyClientFlag, cascade='all, delete-orphan')

    def __init__(self,
                 company_name=None,
                 company_name_kana=None,
                 company_short_name=None,
                 contract_date=None,
                 postal_code=None,
                 address=None,
                 phone=None,
                 fax=None,
                 client_code=None,
                 bp_code=None,
                 billing_site=None,
                 payment_site=None,
                 billing_tax=None,
                 payment_tax=None,
                 bank_id=None,
                 bank_holiday_flag=None,
                 remarks=None,
                 print_name=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Company, self).__init__(created_at, created_user, updated_at, updated_user)
        self.company_name = company_name
        self.company_name_kana = company_name_kana
        self.company_short_name = company_short_name
        self.contract_date = contract_date
        self.postal_code = postal_code
        self.address = address
        self.phone = phone
        self.fax = fax
        self.client_code = client_code
        self.bp_code = bp_code
        self.billing_site = billing_site
        self.payment_site = payment_site
        self.billing_tax = billing_tax
        self.payment_tax = payment_tax
        self.bank_id = bank_id
        self.bank_holiday_flag = bank_holiday_flag
        self.remarks = remarks
        self.print_name = print_name

    def __repr__(self):
        return "<Company:" + \
                "'id='{}".format(self.id) + \
                "', company_name='{}".format(self.company_name) + \
                "', company_name_kana='{}".format(self.company_name_kana) + \
                "', company_short_name='{}".format(self.company_short_name) + \
                "', contract_date='{}".format(self.contract_date) + \
                "', postal_code='{}".format(self.postal_code) + \
                "', address='{}".format(self.address) + \
                "', phone='{}".format(self.phone) + \
                "', fax='{}".format(self.fax) + \
                "', client_code='{}".format(self.client_code) + \
                "', bp_code='{}".format(self.bp_code) + \
                "', billing_site='{}".format(self.billing_site) + \
                "', payment_site='{}".format(self.payment_site) + \
                "', billing_tax='{}".format(self.payment_tax) + \
                "', payment_tax='{}".format(self.payment_tax) + \
                "', bank='{}".format(self.bank) + \
                "', bank_holiday_flag='{}".format(self.bank_holiday_flag) + \
                "', remarks='{}".format(self.remarks) + \
                "', print_name='{}".format(self.print_name) + \
                "', company_client_flags='{}".format(self.company_client_flags) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

    def is_bp(self):
        for company_client_flag in self.company_client_flags:
            if company_client_flag.client_flag == ClientFlag.bp:
                return True
        return False

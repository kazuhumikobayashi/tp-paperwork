from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from application import db
from application.domain.model.bank import Bank
from application.domain.model.base_model import BaseModel
from application.domain.model.company_client_flag import CompanyClientFlag


class Company(BaseModel, db.Model):
    __tablename__ = 'companies'
    PER_PAGE = 10

    company_name = Column(String(128))
    company_name_kana = Column(String(128))
    company_name_abbreviated = Column(String(128))
    contract_date = Column(Date, nullable=False)
    postal_code = Column(String(32))
    address1 = Column(String(1024))
    phone = Column(String(32))
    fax = Column(String(32))
    payment_site = Column(Integer)
    receipt_site = Column(Integer)
    payment_tax = Column(String(4))
    receipt_tax = Column(String(4))
    bank_id = Column(Integer, ForeignKey("banks.id"))
    remarks = Column(String(1024))

    bank = relationship(Bank, lazy='joined')
    company_client_flags = relationship(CompanyClientFlag, cascade='all, delete-orphan')

    def __init__(self,
                 company_name=None,
                 company_name_kana=None,
                 company_name_abbreviated=None,
                 contract_date=None,
                 postal_code=None,
                 address1=None,
                 phone=None,
                 fax=None,
                 payment_site=None,
                 receipt_site=None,
                 payment_tax=None,
                 receipt_tax=None,
                 bank_id=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Company, self).__init__(created_at, created_user, updated_at, updated_user)
        self.company_name = company_name
        self.company_name_kana = company_name_kana
        self.company_name_abbreviated = company_name_abbreviated
        self.contract_date = contract_date
        self.postal_code = postal_code
        self.address1 = address1
        self.phone = phone
        self.fax = fax
        self.payment_site = payment_site
        self.receipt_site = receipt_site
        self.payment_tax = payment_tax
        self.receipt_tax = receipt_tax
        self.bank_id = bank_id
        self.remarks = remarks

    def __repr__(self):
        return "<Company:" + \
                "'id='{}".format(self.id) + \
                "', company_name='{}".format(self.company_name) + \
                "', company_name_kana='{}".format(self.company_name_kana) + \
                "', company_name_abbreviated='{}".format(self.company_name_abbreviated) + \
                "', contract_date='{}".format(self.contract_date) + \
                "', postal_code='{}".format(self.postal_code) + \
                "', address1='{}".format(self.address1) + \
                "', phone='{}".format(self.phone) + \
                "', fax='{}".format(self.fax) + \
                "', payment_site='{}".format(self.payment_site) + \
                "', receipt_site='{}".format(self.receipt_site) + \
                "', payment_tax='{}".format(self.receipt_tax) + \
                "', receipt_tax='{}".format(self.receipt_tax) + \
                "', bank='{}".format(self.bank) + \
                "', remarks='{}".format(self.remarks) + \
                "', company_client_flags='{}".format(self.company_client_flags) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

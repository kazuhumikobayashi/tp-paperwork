from sqlalchemy import Column, Integer, String, Date

from application import db
from application.domain.model.base_model import BaseModel


class Company(BaseModel, db.Model):
    __tablename__ = 'companies'
    PER_PAGE = 10

    company_code = Column(String(32), nullable=False)
    company_name = Column(String(128))
    company_name_kana = Column(String(128))
    trade_name = Column(String(32))
    trade_name_position = Column(String(1))
    client_flg = Column(String(1), nullable=False)
    consignment_flg = Column(String(1), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    postal_code = Column(String(32))
    address1 = Column(String(1024))
    address2 = Column(String(1024))
    phone = Column(String(32))
    fax = Column(String(32))
    payment_site = Column(Integer)
    receipt_site = Column(Integer)
    tax = Column(String(1), nullable=False)
    remarks = Column(String(1024))

    def __init__(self,
                 company_code=None,
                 company_name=None,
                 company_name_kana=None,
                 trade_name=None,
                 trade_name_position=None,
                 client_flg=None,
                 consignment_flg=None,
                 start_date=None,
                 end_date=None,
                 postal_code=None,
                 address1=None,
                 address2=None,
                 phone=None,
                 fax=None,
                 payment_site=None,
                 receipt_site=None,
                 tax=None,
                 remarks=None,
                 created_at=None,
                 created_user=None,
                 updated_at=None,
                 updated_user=None):
        super(Company, self).__init__(created_at, created_user, updated_at, updated_user)
        self.company_code = company_code
        self.company_name = company_name
        self.company_name_kana = company_name_kana
        self.trade_name = trade_name
        self.trade_name_position = trade_name_position
        self.client_flg = client_flg
        self.consignment_flg = consignment_flg
        self.start_date = start_date
        self.end_date = end_date
        self.postal_code = postal_code
        self.address1 = address1
        self.address2 = address2
        self.phone = phone
        self.fax = fax
        self.payment_site = payment_site
        self.receipt_site = receipt_site
        self.tax = tax
        self.remarks = remarks

    def __repr__(self):
        return "<Company:" + \
                "'id='{}".format(self.id) + \
                "', company_code='{}".format(self.company_code) + \
                "', company_name='{}".format(self.company_name) + \
                "', company_name_kana='{}".format(self.company_name_kana) + \
                "', trade_name='{}".format(self.trade_name) + \
                "', trade_name_position='{}".format(self.trade_name_position) + \
                "', client_flg='{}".format(self.client_flg) + \
                "', consignment_flg='{}".format(self.consignment_flg) + \
                "', start_date='{}".format(self.start_date) + \
                "', end_date='{}".format(self.end_date) + \
                "', postal_code='{}".format(self.postal_code) + \
                "', address1='{}".format(self.address1) + \
                "', address2='{}".format(self.address2) + \
                "', phone='{}".format(self.phone) + \
                "', fax='{}".format(self.fax) + \
                "', payment_site='{}".format(self.payment_site) + \
                "', receipt_site='{}".format(self.receipt_site) + \
                "', tax='{}".format(self.tax) + \
                "', remarks='{}".format(self.remarks) + \
                "', created_at='{}".format(self.created_at) + \
                "', created_user='{}".format(self.created_user) + \
                "', updated_at='{}".format(self.updated_at) + \
                "', updated_user='{}".format(self.updated_user) + \
                "'>"

from flask_wtf import FlaskForm
from wtforms import validators, StringField, SelectField, BooleanField, RadioField

from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length, DataRequired


class CompanyForm(FlaskForm):
    id = IntegerField('Id')
    company_code = StringField('会社コード', [DataRequired(), Length(max=32)])
    company_name = StringField('会社名', [Length(max=128)], filters=[lambda x: x or None])
    company_name_kana = StringField('会社名（カナ）', [Length(max=128)], filters=[lambda x: x or None])
    trade_name = StringField('商号', [Length(max=32)], filters=[lambda x: x or None])
    trade_name_position = SelectField('商号位置',
                                      choices=[('', ''), ('1', '前'), ('2', '後ろ')],
                                      filters = [lambda x: x or None],
                                      render_kw={"data-minimum-results-for-search": "Infinity"})
    client_flg = SelectField('顧客フラグ', choices=[('', ''), ('1', '顧客')],
                             filters = [lambda x: x or '0'],
                             render_kw={"data-minimum-results-for-search": "Infinity"})
    consignment_flg = SelectField('委託フラグ', choices=[('', ''), ('1', '委託')],
                                  filters=[lambda x: x or '0'],
                                  render_kw = {"data-minimum-results-for-search": "Infinity"})
    start_date = DateField('取引開始年月', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    end_date = DateField('取引終了年月', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    postal_code = StringField('郵便番号', [Length(max=32)], filters=[lambda x: x or None])
    address1 = StringField('住所１', [Length(max=1024)], filters=[lambda x: x or None])
    address2 = StringField('住所２', [Length(max=1024)], filters=[lambda x: x or None])
    phone = StringField('電話番号', [Length(max=32)], filters=[lambda x: x or None])
    fax = StringField('Fax番号', [Length(max=32)], filters=[lambda x: x or None])
    payment_site = IntegerField('入金サイト')
    receipt_site = IntegerField('支払サイト')
    tax = SelectField('税区分', [DataRequired(), Length(max=1)],
                      choices=[('', ''), ('1', '消費税あり'), ('0', '消費税なし')],
                      render_kw={"data-minimum-results-for-search": "Infinity"})
    remarks = StringField('備考', [Length(max=1024)], filters=[lambda x: x or None])

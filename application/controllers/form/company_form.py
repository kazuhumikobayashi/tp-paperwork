from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField, validators, RadioField
from wtforms.validators import ValidationError

from application.controllers.form.fields import IntegerField, DateField, RadioField
from application.controllers.form.validators import Length, DataRequired
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.holiday_flag import HolidayFlag
from application.domain.model.immutables.site import Site
from application.domain.model.immutables.tax import Tax
from application.service.company_service import CompanyService

service = CompanyService()


def required_if_client(form, field):
    if str(ClientFlag.client) in form.client_flag.data and not field.data:
        raise ValidationError('顧客の場合、入力必須です。')


def required_if_bp(form, field):
    if str(ClientFlag.bp) in form.client_flag.data and not field.data:
        raise ValidationError('BP所属の場合、入力必須です。')


class CompanyForm(FlaskForm):
    id = IntegerField('Id')
    company_name = StringField('会社名称（必須）', [DataRequired(), Length(max=128)], filters=[lambda x: x or None])
    company_name_kana = StringField('会社名称カナ', [Length(max=128)], filters=[lambda x: x or None])
    company_short_name = StringField('会社略称', [Length(max=32)], filters=[lambda x: x or None])
    client_flag = SelectMultipleField('顧客フラグ（必須）', [DataRequired()])
    contract_date = DateField('基本契約日', [validators.optional()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    postal_code = StringField('郵便番号', [Length(max=32)], filters=[lambda x: x or None])
    address = StringField('住所', [Length(max=1024)], filters=[lambda x: x or None])
    phone = StringField('電話番号', [Length(max=32)], filters=[lambda x: x or None])
    fax = StringField('Fax番号', [Length(max=32)], filters=[lambda x: x or None])
    client_code = StringField('顧客コード（顧客フラグ＝顧客の時、必須）',
                              [Length(max=128), required_if_client],
                              filters=[lambda x: x or None])
    bp_code = StringField('協力会社コード（顧客フラグ＝BP所属の時、必須）', 
                          [Length(max=128), required_if_bp], 
                          filters=[lambda x: x or None])
    payment_site = SelectField('入金サイト（顧客フラグ＝顧客の時、必須）',
                               [required_if_client],
                               choices=Site.get_site_for_select(),
                               render_kw={"data-minimum-results-for-search": "Infinity"})
    receipt_site = SelectField('支払サイト（顧客フラグ＝BP所属の時、必須）',
                               [required_if_bp],
                               choices=Site.get_site_for_select(),
                               render_kw={"data-minimum-results-for-search": "Infinity"})
    payment_tax = SelectField('入金消費税（顧客フラグ＝顧客の時、必須）',
                              [Length(max=8), required_if_client],
                              choices=Tax.get_type_for_select(),
                              render_kw={"data-minimum-results-for-search": "Infinity"})
    receipt_tax = SelectField('支払消費税（顧客フラグ＝BP所属の時、必須）',
                              [Length(max=8), required_if_bp],
                              choices=Tax.get_type_for_select(),
                              render_kw={"data-minimum-results-for-search": "Infinity"})
    bank_id = SelectField('振込先銀行（顧客フラグ＝顧客の時、必須）',
                          [required_if_client],
                          render_kw={"data-minimum-results-for-search": "Infinity"})
    bank_holiday_flag = RadioField('振込先銀行休日時フラグ（顧客フラグ＝顧客の時、必須）', 
                                   [required_if_client],
                                   choices=HolidayFlag.get_flag_for_radio())
    remarks = TextAreaField('備考', [Length(max=1024)], filters=[lambda x: x or None])
    print_name = TextAreaField('印刷用宛名', [Length(max=1024)], filters=[lambda x: x or None])
    
    def validate_client_flag(self, field):
        companies = service.find_by_client_flag([ClientFlag.our_company.value])
        if str(ClientFlag.our_company) in field.data and len(companies) != 0 and companies[0].id != self.id.data:
            raise ValidationError('「自社」は登録できません。')

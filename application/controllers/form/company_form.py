from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField, validators
from wtforms.validators import ValidationError

from application.const import TAX_CLASSIFICATION, ClientFlag
from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length, DataRequired
from application.service.company_service import CompanyService

service = CompanyService()


class CompanyForm(FlaskForm):
    id = IntegerField('Id')
    company_name = StringField('会社名称（必須）', [DataRequired(), Length(max=128)], filters=[lambda x: x or None])
    company_name_kana = StringField('会社名称カナ', [Length(max=128)], filters=[lambda x: x or None])
    company_short_name = StringField('会社略称', [Length(max=32)], filters=[lambda x: x or None])
    client_flag = SelectMultipleField('顧客フラグ（必須）', [DataRequired(), Length(max=2048)], coerce=int)
    contract_date = DateField('基本契約日', [validators.optional()], format='%Y/%m/%d')
    postal_code = StringField('郵便番号', [Length(max=32)], filters=[lambda x: x or None])
    address = StringField('住所', [Length(max=1024)], filters=[lambda x: x or None])
    phone = StringField('電話番号', [Length(max=32)], filters=[lambda x: x or None])
    fax = StringField('Fax番号', [Length(max=32)], filters=[lambda x: x or None])
    payment_site = IntegerField('入金サイト（顧客フラグ＝顧客の時、必須）')
    receipt_site = IntegerField('支払サイト（顧客フラグ＝BP所属の時、必須）')
    payment_tax = SelectField('入金消費税区分（顧客フラグ＝顧客の時、必須）',
                              [Length(max=8)],
                              choices=TAX_CLASSIFICATION,
                              render_kw={"data-minimum-results-for-search": "Infinity"})
    receipt_tax = SelectField('支払消費税区分（顧客フラグ＝BP所属の時、必須）',
                              [Length(max=8)],
                              choices=TAX_CLASSIFICATION,
                              render_kw={"data-minimum-results-for-search": "Infinity"})
    bank_id = SelectField('振込先銀行（顧客フラグ＝顧客の時、必須）',
                          render_kw={"data-minimum-results-for-search": "Infinity"})
    remarks = TextAreaField('備考', [Length(max=1024)], filters=[lambda x: x or None])
    
    def validate_client_flag(self, field):
        companies = service.find_by_client_flag_id(ClientFlag.OUR_COMPANY.value)
        if ClientFlag.OUR_COMPANY.value in field.data and len(companies) != 0 and companies[0].id != self.id.data:
            raise ValidationError('「自社」は登録できません。')
    
    def validate_payment_site(self, field):
        if ClientFlag.CLIENT.value in self.client_flag.data and field.data is None:
            raise ValidationError('顧客の場合、入力必須です。')

    def validate_receipt_site(self, field):
        if ClientFlag.BP.value in self.client_flag.data and field.data is None:
            raise ValidationError('BP所属の場合、入力必須です。')

    def validate_payment_tax(self, field):
        if ClientFlag.CLIENT.value in self.client_flag.data and field.data == '':
            raise ValidationError('顧客の場合、入力必須です。')

    def validate_receipt_tax(self, field):
        if ClientFlag.BP.value in self.client_flag.data and field.data == '':
            raise ValidationError('BP所属の場合、入力必須です。')

    def validate_bank_id(self, field):
        if ClientFlag.CLIENT.value in self.client_flag.data and field.data == '':
            raise ValidationError('顧客の場合、入力必須です。')

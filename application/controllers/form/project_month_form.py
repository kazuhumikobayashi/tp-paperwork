from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, ValidationError, DateTimeField, SelectField

from application.controllers.form.fields import IntegerField, DateField
from application.controllers.form.validators import Length, DataRequired
from application.domain.model.immutables.tax import Tax
from application.domain.repository.project_month_repository import ProjectMonthRepository

project_month_repository = ProjectMonthRepository()


class ProjectMonthForm(FlaskForm):
    id = IntegerField('プロジェクト年月ID')
    project_id = IntegerField('プロジェクトID')
    client_billing_no = StringField('顧客請求書No', [Length(max=64)], filters=[lambda x: x or None])
    billing_confirmation_money = IntegerField('請求確定金額（請求明細金額の合計）', render_kw={"readonly": "readonly"})
    billing_tax = SelectField('消費税',
                              [DataRequired()],
                              choices=Tax.get_type_for_select(),
                              render_kw={"title": "消費税"})
    billing_transportation = IntegerField('請求交通費等（請求明細交通費等の合計）', render_kw={"readonly": "readonly"})
    billing_printed_date = DateField('請求書発行日', format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    deposit_date = DateField('入金予定日', format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    remarks = TextAreaField('備考', [Length(max=1024)], filters=[lambda x: x or None])
    project_month = DateField('プロジェクト年月', format='%Y/%m/%d')
    updated_user = StringField('更新者')
    updated_at = DateTimeField('更新日')

    def validate_client_billing_no(self, field):
        project_month = project_month_repository.find_by_client_billing_no(client_billing_no=field.data)
        if project_month and project_month.id != self.id.data:
            raise ValidationError('この顧客請求書Noは既に登録されています。')

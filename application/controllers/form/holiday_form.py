from flask_wtf import FlaskForm
from wtforms import ValidationError, IntegerField, StringField, DateTimeField

from application.controllers.form.fields import DateField
from application.controllers.form.validators import Length, DataRequired
from application.domain.repository.holiday_repository import HolidayRepository

repository = HolidayRepository()


class HolidayForm(FlaskForm):
    id = IntegerField('Id')
    holiday = DateField('祝日（必須）', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})
    holiday_name = StringField('祝日名称', [Length(max=128)], filters=[lambda x: x or None])
    updated_user = StringField('更新者')
    updated_at = DateTimeField('更新日')

    def validate_holiday(self, field):
        holiday = repository.find_by_date(date=field.data)
        if holiday and holiday.id != self.id.data:
            raise ValidationError('この日は既に登録されています。')

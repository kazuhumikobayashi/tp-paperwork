from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import ValidationError

from application.controllers.form.fields import IntegerField
from application.controllers.form.validators import Length, DataRequired
from application.domain.repository.business_category_repository import BusinessCategoryRepository

repository = BusinessCategoryRepository()


class BusinessCategoryForm(FlaskForm):
    id = IntegerField('Id')
    business_category_name = StringField('業種（必須）', [DataRequired(), Length(max=32)])

    def validate_business_category_name(self, field):
        business_category = repository.find_by_name(field.data)
        if business_category and business_category.id != self.id.data:
            raise ValidationError('同じ名称の業種が既に登録されています。')

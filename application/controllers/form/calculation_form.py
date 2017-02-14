from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import ValidationError

from application.const import FORMULA
from application.controllers.form.fields import IntegerField
from application.controllers.form.validators import DataRequired, InputRequired
from application.domain.repository.calculation_repository import CalculationRepository

repository = CalculationRepository()


class CalculationForm(FlaskForm):
    id = IntegerField('id')
    amount = IntegerField('金額',
                          [InputRequired()])
    formula = SelectField('計算式',
                          [DataRequired()],
                          choices=FORMULA,
                          render_kw={"data-minimum-results-for-search": "Infinity"})

    def validate_amount(self, field):
        calculation = repository.find_by_amount_and_formula(amount=field.data, formula=self.formula.data)
        if calculation and calculation.id != self.id.data:
            raise ValidationError('同じ計算式が既に登録されています。')

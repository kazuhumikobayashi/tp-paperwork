from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, RadioField, validators
from wtforms.validators import ValidationError

from application.controllers.form.fields import IntegerField, BeginningOfMonthField, EndOfMonthField
from application.controllers.form.validators import Length, DataRequired, LessThan, InputRequired
from application.domain.model.immutables.fraction import Fraction
from application.domain.model.immutables.round import Round
from application.domain.model.immutables.rule import Rule
from application.domain.model.immutables.tax import Tax
from application.domain.repository.engineer_history_repository import EngineerHistoryRepository

repository = EngineerHistoryRepository()


def required_if_variable(form, field):
    if form.payment_rule.data == str(Rule.variable) and field.data is None:
        raise ValidationError('支払いのルールが変動の場合、入力必須です。')


class EngineerHistoryForm(FlaskForm):
    id = IntegerField('Id')
    payment_start_day = BeginningOfMonthField('支払い契約開始年月（必須）',
                                              [DataRequired(), LessThan('payment_end_day', '支払い契約終了年月より前の年月にして下さい。')],
                                              format='%Y/%m',
                                              render_kw={"autocomplete": "off"})
    payment_end_day = EndOfMonthField('支払い契約終了年月（必須）',
                                      [DataRequired()],
                                      format='%Y/%m',
                                      render_kw={"autocomplete": "off"})
    payment_site = IntegerField('支払サイト', [validators.optional()], render_kw={"disabled": "disabled"})
    payment_tax = SelectField('支払消費税区分',
                              [validators.optional()],
                              choices=Tax.get_type_for_select(),
                              filters=[lambda x: x or None],
                              render_kw={"data-minimum-results-for-search": "Infinity", "disabled": "disabled"})
    payment_per_month = IntegerField('支払単価（必須）', [InputRequired()])
    payment_rule = RadioField('支払ルール（必須）',
                              [DataRequired()],
                              choices=Rule.get_rule_for_select(),
                              filters=[lambda x: x or None])
    payment_bottom_base_hour = IntegerField('支払下限基準時間（必須）')
    payment_top_base_hour = IntegerField('支払上限基準時間（必須）')
    payment_free_base_hour = StringField('支払フリー入力基準時間（必須）',
                                         [Length(max=128)],
                                         filters=[lambda x: x or None])
    payment_per_hour = StringField('支払時間単価（必須）',
                                   [Length(max=128), required_if_variable],
                                   filters=[lambda x: x or None])
    payment_per_bottom_hour = IntegerField('支払△下限時間単価（必須）', [required_if_variable])
    payment_per_top_hour = IntegerField('支払＋下限時間単価', [required_if_variable])
    payment_fraction = SelectField('支払端数金額',
                                   [validators.Optional()],
                                   choices=Fraction.get_fraction_for_select(),
                                   filters=[lambda x: x or None],
                                   render_kw={"data-minimum-results-for-search": "Infinity"})
    payment_fraction_rule = SelectField('支払端数ルール',
                                        [validators.Optional()],
                                        choices=Round.get_round_for_select(),
                                        filters=[lambda x: x or None],
                                        render_kw={"data-minimum-results-for-search": "Infinity"})
    payment_condition = TextAreaField('支払条件', [Length(max=1024)])
    remarks = TextAreaField('その他特記事項', [Length(max=1024)])

    def validate_payment_start_day(self, field):
        engineer_history = repository.find_by_id(self.id.data)
        if engineer_history and engineer_history.payment_end_day is not None \
                and field.data != engineer_history.payment_start_day and field.data < engineer_history.payment_end_day:
            raise ValidationError('前回の支払い契約終了年月「'
                                  + engineer_history.payment_end_day.strftime('%Y/%m')
                                  + '」よりの前の年月で更新できません。')

    def validate_payment_bottom_base_hour(self, field):
        # 支払いのルールが変動の時、フリー時間が空ならエラー
        if self.payment_rule.data == str(Rule.variable) and field.data is None \
                and self.payment_free_base_hour.data is None:
            raise ValidationError('支払いのルールが変動の場合、入力必須です。')

    def validate_payment_top_base_hour(self, field):
        # 支払いのルールが変動の時、フリー時間が空ならエラー
        if self.payment_rule.data == str(Rule.variable) and field.data is None \
                and self.payment_free_base_hour.data is None:
            raise ValidationError('支払いのルールが変動の場合、入力必須です。')

    def validate_payment_free_base_hour(self, field):
        # 支払いのルールが変動の時、下限時間または上限時間が空ならエラー
        if self.payment_rule.data == str(Rule.variable) and field.data is None \
                and self.payment_bottom_base_hour.data is None \
                and self.payment_top_base_hour.data is None:
            raise ValidationError('支払いのルールが変動の場合、入力必須です。')

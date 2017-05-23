from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, RadioField, validators
from wtforms.validators import ValidationError

from application.const import TAX_CLASSIFICATION, RECEIPT_RULE, ReceiptRule, \
                              FRACTION_CALCULATION1, FRACTION_CALCULATION2
from application.controllers.form.fields import IntegerField, BeginningOfMonthField, EndOfMonthField
from application.controllers.form.validators import Length, DataRequired, LessThan
from application.domain.repository.engineer_history_repository import EngineerHistoryRepository

repository = EngineerHistoryRepository()


def required_if_variable(form, field):
    if form.receipt_rule.data == ReceiptRule.VARIABLE.value and field.data is None:
        raise ValidationError('支払いのルールが変動の場合、入力必須です。')


class EngineerHistoryForm(FlaskForm):
    id = IntegerField('Id')
    receipt_start_day = BeginningOfMonthField('支払い契約開始年月（必須）',
                                              [DataRequired(), LessThan('receipt_end_day', '支払い契約終了年月より前の年月にして下さい。')],
                                              format='%Y/%m',
                                              render_kw={"autocomplete": "off"})
    receipt_end_day = EndOfMonthField('支払い契約終了年月（必須）',
                                      [DataRequired()],
                                      format='%Y/%m',
                                      render_kw={"autocomplete": "off"})
    receipt_site = IntegerField('支払サイト', [validators.optional()], render_kw={"disabled": "disabled"})
    receipt_tax = SelectField('支払消費税区分',
                              [validators.optional()],
                              choices=TAX_CLASSIFICATION,
                              filters=[lambda x: x or None],
                              render_kw={"data-minimum-results-for-search": "Infinity", "disabled": "disabled"})
    receipt_per_month = IntegerField('支払単価（必須）', [DataRequired()])
    receipt_rule = RadioField('支払ルール（必須）',
                              [DataRequired()],
                              choices=RECEIPT_RULE,
                              filters=[lambda x: x or None])
    receipt_bottom_base_hour = IntegerField('支払下限基準時間（必須）')
    receipt_top_base_hour = IntegerField('支払上限基準時間（必須）')
    receipt_free_base_hour = StringField('支払フリー入力基準時間（必須）',
                                         [Length(max=128)],
                                         filters=[lambda x: x or None])
    receipt_per_hour = StringField('支払時間単価（必須）',
                                   [Length(max=128), required_if_variable],
                                   filters=[lambda x: x or None])
    receipt_per_bottom_hour = IntegerField('支払△下限時間単価（必須）', [required_if_variable])
    receipt_per_top_hour = IntegerField('支払＋下限時間単価', [required_if_variable])
    receipt_fraction = IntegerField('支払端数金額')
    receipt_fraction_calculation1 = SelectField('支払端数計算式１',
                                                [validators.Optional()],
                                                choices=FRACTION_CALCULATION1,
                                                filters=[lambda x: x or None],
                                                render_kw={"data-minimum-results-for-search": "Infinity"})
    receipt_fraction_calculation2 = SelectField('支払端数計算式２',
                                                [validators.Optional()],
                                                choices=FRACTION_CALCULATION2,
                                                filters=[lambda x: x or None],
                                                render_kw={"data-minimum-results-for-search": "Infinity"})
    receipt_condition = TextAreaField('支払条件', [Length(max=1024)])
    remarks = TextAreaField('その他特記事項', [Length(max=1024)])

    def validate_receipt_start_day(self, field):
        engineer_history = repository.find_by_id(self.id.data)
        if engineer_history and engineer_history.receipt_end_day is not None \
                and field.data != engineer_history.receipt_start_day and field.data < engineer_history.receipt_end_day:
            raise ValidationError('前回の支払い契約終了年月「'
                                  + engineer_history.receipt_end_day.strftime('%Y/%m')
                                  + '」よりの前の年月で更新できません。')

    def validate_receipt_bottom_base_hour(self, field):
        # 支払いのルールが変動の時、フリー時間が空ならエラー
        if self.receipt_rule.data == ReceiptRule.VARIABLE.value and field.data is None \
                and self.receipt_free_base_hour.data is None:
            raise ValidationError('支払いのルールが変動の場合、入力必須です。')

    def validate_receipt_top_base_hour(self, field):
        # 支払いのルールが変動の時、フリー時間が空ならエラー
        if self.receipt_rule.data == ReceiptRule.VARIABLE.value and field.data is None \
                and self.receipt_free_base_hour.data is None:
            raise ValidationError('支払いのルールが変動の場合、入力必須です。')

    def validate_receipt_free_base_hour(self, field):
        # 支払いのルールが変動の時、下限時間または上限時間が空ならエラー
        if self.receipt_rule.data == ReceiptRule.VARIABLE.value and field.data is None \
                and self.receipt_bottom_base_hour.data is None \
                and self.receipt_top_base_hour.data is None:
            raise ValidationError('支払いのルールが変動の場合、入力必須です。')

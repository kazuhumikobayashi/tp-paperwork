from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, StringField, RadioField, DateField, validators, HiddenField

from application.controllers.form.fields import IntegerField, DecimalField
from application.controllers.form.validators import Length
from application.domain.model.immutables.fraction import Fraction
from application.domain.model.immutables.round import Round
from application.domain.model.immutables.rule import Rule


class ResultForm(FlaskForm):
    result_month = DateField('実績年月', [validators.optional()], format='%Y/%m/%d')
    engineer_name = StringField('技術者名称', render_kw={"disabled": "disabled"})
    work_time = DecimalField('実稼働時間')
    billing_subtraction_hours = IntegerField('請求差分時間（基準時間と実稼働時間の差分）',
                                             render_kw={"disabled": "disabled"})
    billing_subtraction_money = IntegerField('請求差分金額（差分時間に時間単価を掛けた金額）',
                                             render_kw={"disabled": "disabled"})
    billing_estimated_money = IntegerField('請求予定金額（単価と差分金額の合計）', render_kw={"disabled": "disabled"})
    billing_transportation = IntegerField('請求交通費等_個別')
    billing_adjustments = IntegerField('請求調整金額_個別')
    billing_confirmation_number = StringField('請求確定数量_個別（請求書に出力する人月。基本1.0人月）',
                                              [Length(max=128)],
                                              filters=[lambda x: x or None])
    billing_confirmation_money = IntegerField('請求確定金額_個別（予定金額と調整金額の合計）',
                                              render_kw={"readonly": "readonly"})
    payment_subtraction_hours = IntegerField('支払差分時間（基準時間と実稼働時間の差分）',
                                             render_kw={"disabled": "disabled"})
    payment_subtraction_money = IntegerField('支払差分金額（差分時間に時間単価を掛けた金額）',
                                             render_kw={"disabled": "disabled"})
    payment_estimated_money = IntegerField('支払予定金額（単価と差分金額の合計）', render_kw={"disabled": "disabled"})
    payment_transportation = IntegerField('支払交通費等_個別')
    payment_adjustments = IntegerField('支払調整金額_個別')
    payment_expected_date = DateField('支払予定日',
                                      [validators.optional()],
                                      format='%Y/%m/%d',
                                      render_kw={"autocomplete": "off"})
    payment_confirmation_money = IntegerField('支払確定金額_個別（予定金額と調整金額の合計）',
                                              render_kw={"readonly": "readonly"})
    remarks = TextAreaField('備考', [Length(max=1024)], filters=[lambda x: x or None])


class ProjectDetailInResultForm(FlaskForm):
    project_id = HiddenField('プロジェクトId')
    billing_per_month = IntegerField('請求単価', render_kw={"disabled": "disabled"})
    billing_rule = RadioField('請求ルール',
                              [validators.optional()],
                              choices=Rule.get_rule_for_select(),
                              render_kw={"disabled": "disabled"})
    billing_bottom_base_hour = IntegerField('請求下限基準時間', render_kw={"disabled": "disabled"})
    billing_top_base_hour = IntegerField('請求上限基準時間', render_kw={"disabled": "disabled"})
    billing_free_base_hour = StringField('請求フリー基準時間', [Length(max=128)], render_kw={"disabled": "disabled"})
    billing_per_hour = StringField('請求時間単価', [Length(max=128)], render_kw={"disabled": "disabled"})
    billing_per_bottom_hour = IntegerField('請求△下限時間単価', render_kw={"disabled": "disabled"})
    billing_per_top_hour = IntegerField('請求＋上限時間単価', render_kw={"disabled": "disabled"})
    billing_fraction = SelectField('請求端数金額',
                                   [validators.Optional()],
                                   choices=Fraction.get_fraction_for_select(),
                                   filters=[lambda x: x or None],
                                   render_kw={"data-minimum-results-for-search": "Infinity", "disabled": "disabled"})
    billing_fraction_rule = SelectField('請求端数ルール',
                                        [validators.optional()],
                                        choices=Round.get_round_for_select(),
                                        render_kw={"data-minimum-results-for-search": "Infinity",
                                                   "disabled": "disabled"})


class EngineerHistoryInResultForm(FlaskForm):
    payment_per_month = IntegerField('支払単価', render_kw={"disabled": "disabled"})
    payment_rule = RadioField('支払ルール',
                              [validators.optional()],
                              choices=Rule.get_rule_for_select(),
                              render_kw={"disabled": "disabled"})
    payment_bottom_base_hour = IntegerField('支払下限基準時間', render_kw={"disabled": "disabled"})
    payment_top_base_hour = IntegerField('支払上限基準時間', render_kw={"disabled": "disabled"})
    payment_free_base_hour = StringField('支払フリー基準時間', [Length(max=128)], render_kw={"disabled": "disabled"})
    payment_per_hour = StringField('支払時間単価', [Length(max=128)], render_kw={"disabled": "disabled"})
    payment_per_bottom_hour = IntegerField('支払△下限時間単価', render_kw={"disabled": "disabled"})
    payment_per_top_hour = IntegerField('支払＋上限時間単価', render_kw={"disabled": "disabled"})
    payment_fraction = SelectField('支払端数金額',
                                   [validators.Optional()],
                                   choices=Fraction.get_fraction_for_select(),
                                   filters=[lambda x: x or None],
                                   render_kw={"data-minimum-results-for-search": "Infinity", "disabled": "disabled"})
    payment_fraction_rule = SelectField('請求端数ルール',
                                        [validators.optional()],
                                        choices=Round.get_round_for_select(),
                                        render_kw={"data-minimum-results-for-search": "Infinity",
                                                   "disabled": "disabled"})

from flask_wtf import FlaskForm
from wtforms import validators, HiddenField, StringField, DateField, SelectField
from wtforms.validators import ValidationError

from application.controllers.form.fields import IntegerField, DateField, RadioField
from application.controllers.form.validators import Length, DataRequired
from application.domain.model.immutables.detail_type import DetailType
from application.domain.model.immutables.rule import Rule


# 明細区分で作業者を選択した場合、入力必須にする。
def required_if_engineer(form, field):
    if form.detail_type.data == str(DetailType.engineer) and not field.data:
        raise ValidationError('入力必須項目です。')


# 明細区分で作業を選択した場合、入力必須にする。
def required_if_work(form, field):
    if form.detail_type.data == str(DetailType.work) and not field.data:
        raise ValidationError('入力必須項目です。')


# 請求ルールで変動を選択した場合、入力必須にする。
def required_if_variable(form, field):
    if form.billing_rule.data == str(Rule.variable) and not field.data:
        raise ValidationError('入力必須項目です。')


class ProjectDetailForm(FlaskForm):
    id = HiddenField('Id')
    detail_type = RadioField('明細区分（必須）',
                             [DataRequired()],
                             choices=DetailType.get_type_for_select(),
                             render_kw={"disabled": "disabled"})
    work_name = StringField('作業名称（必須）', [Length(max=128), required_if_work])
    engineer_id = SelectField('技術者名称（必須）',
                              [required_if_engineer])
    company = StringField('所属会社', render_kw={"disabled": "disabled"})
    billing_money = IntegerField('請求金額（必須）', [DataRequired()])
    remarks = StringField('備考', [Length(max=1024)])
    billing_start_day = DateField('請求契約開始年月（必須）',
                                  [required_if_engineer],
                                  format='%Y/%m',
                                  render_kw={"autocomplete": "off"})
    billing_end_day = DateField('請求契約終了年月（必須）',
                                [required_if_engineer],
                                format='%Y/%m',
                                render_kw={"autocomplete": "off"})
    billing_per_month = IntegerField('請求単価（必須）', [required_if_engineer])
    billing_rule = RadioField('請求ルール（必須）',
                              [required_if_engineer],
                              choices=Rule.get_rule_for_select())
    billing_bottom_base_hour = IntegerField('請求下限基準時間')
    billing_top_base_hour = IntegerField('請求上限基準時間')
    billing_free_base_hour = StringField('請求フリー入力基準時間',
                                         [Length(max=128)],
                                         filters=[lambda x: x or None])
    billing_per_hour = StringField('請求時間単価', [Length(max=128), required_if_variable])
    billing_per_bottom_hour = IntegerField('請求△下限時間単価', [required_if_variable])
    billing_per_top_hour = IntegerField('請求＋上限時間単価', [required_if_variable])
    billing_fraction = IntegerField('請求端数金額')
    billing_fraction_calculation1 = SelectField('請求端数計算式１',
                                                [validators.Optional()],
                                                choices=[('', ''),
                                                         ('1', '以上'),
                                                         ('2', 'より大きい'),
                                                         ('3', '以下'),
                                                         ('4', '未満')],
                                                render_kw={"data-minimum-results-for-search": "Infinity"})
    billing_fraction_calculation2 = SelectField('請求端数計算式２',
                                                [validators.Optional()],
                                                choices=[('', ''),
                                                         ('1', '切り捨て'),
                                                         ('2', '繰り上げ'),
                                                         ('3', '四捨五入')],
                                                render_kw={"data-minimum-results-for-search": "Infinity"})
    payment_start_day = DateField('支払契約開始年月（必須）',
                                  [validators.Optional()],
                                  format='%Y/%m',
                                  render_kw={"autocomplete": "off", "disabled": "disabled"})
    payment_end_day = DateField('支払契約終了年月（必須）',
                                [validators.Optional()],
                                format='%Y/%m',
                                render_kw={"autocomplete": "off", "disabled": "disabled"})
    payment_per_month = IntegerField('支払単価（必須）', render_kw={"disabled": "disabled"})
    payment_rule = RadioField('支払いルール（必須）',
                              [validators.Optional()],
                              choices=Rule.get_rule_for_select(),
                              render_kw={"disabled": "disabled"})
    payment_bottom_base_hour = IntegerField('支払下限基準時間',
                                            render_kw={"disabled": "disabled"})
    payment_top_base_hour = IntegerField('支払上限基準時間',
                                         render_kw={"disabled": "disabled"})
    payment_free_base_hour = StringField('支払フリー入力基準時間', [Length(max=128)],
                                         render_kw={"disabled": "disabled"})
    payment_per_hour = StringField('支払時間単価', [Length(max=128)],
                                   render_kw={"disabled": "disabled"})
    payment_per_bottom_hour = IntegerField('支払△下限時間単価',
                                           render_kw={"disabled": "disabled"})
    payment_per_top_hour = IntegerField('支払＋上限時間単価',
                                        render_kw={"disabled": "disabled"})
    payment_fraction = IntegerField('支払端数金額',
                                    render_kw={"disabled": "disabled"})
    payment_fraction_calculation1 = SelectField('支払端数計算式１',
                                                [validators.Optional()],
                                                choices=[('', ''),
                                                         ('1', '以上'),
                                                         ('2', 'より大きい'),
                                                         ('3', '以下'),
                                                         ('4', '未満')],
                                                render_kw={"data-minimum-results-for-search": "Infinity",
                                                           "disabled": "disabled"})
    payment_fraction_calculation2 = SelectField('支払端数計算式２',
                                                [validators.Optional()],
                                                choices=[('', ''),
                                                         ('1', '切り捨て'),
                                                         ('2', '繰り上げ'),
                                                         ('3', '四捨五入')],
                                                render_kw={"data-minimum-results-for-search": "Infinity",
                                                           "disabled": "disabled"})
    bp_order_no = StringField('BP注文書No')
    client_order_no_for_bp = StringField('顧客注文書No（BPごと）')

    def validate_billing_bottom_base_hour(self, field):
        # 請求ルールが変動の時、フリー時間が空ならエラー
        if self.billing_rule.data == str(Rule.variable) and field.data is None \
                and self.billing_free_base_hour.data is None:
            raise ValidationError('入力必須項目です。')

    def validate_billing_top_base_hour(self, field):
        # 請求ルールが変動の時、フリー時間が空ならエラー
        if self.billing_rule.data == str(Rule.variable) and field.data is None \
                and self.billing_free_base_hour.data is None:
            raise ValidationError('入力必須項目です。')

    def validate_billing_free_base_hour(self, field):
        # 請求ルールが変動の時、下限時間または上限時間が空ならエラー
        if self.billing_rule.data == str(Rule.variable) and field.data is None \
                and self.billing_bottom_base_hour.data is None \
                and self.billing_top_base_hour.data is None:
            raise ValidationError('入力必須項目です。')

from flask_wtf import FlaskForm
from wtforms import StringField, DateField

from application.controllers.form.fields import DateField
from application.controllers.form.validators import Length, DataRequired, LessThan


class ProjectCreateForm(FlaskForm):
    project_name = StringField('プロジェクト名（必須）', [DataRequired(), Length(max=128)])
    project_name_for_bp = StringField('BP向けプロジェクト名称', [Length(max=128)], filters=[lambda x: x or None])
    start_date = DateField('プロジェクト開始日（必須）',
                           [DataRequired(), LessThan('end_date')],
                           format='%Y/%m/%d',
                           render_kw={"autocomplete": "off"})
    end_date = DateField('プロジェクト終了日（必須）', [DataRequired()], format='%Y/%m/%d', render_kw={"autocomplete": "off"})

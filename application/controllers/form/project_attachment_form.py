from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SelectField
from wtforms import ValidationError

from application.const import get_type_for_select
from application.controllers.form.fields import IntegerField
from application.controllers.form.validators import DataRequired, Length, FileAllowed
from application.domain.model.upload_set import UploadSet

files = UploadSet('files', ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'xlsx', 'xls'])


class ProjectAttachmentForm(FlaskForm):
    id = IntegerField('id')
    project_id = IntegerField('プロジェクトid')
    type = SelectField('区分',
                       [DataRequired()],
                       choices=get_type_for_select(),
                       render_kw={"data-minimum-results-for-search": "Infinity"})
    remarks = StringField('備考', [Length(max=256)])
    filename = StringField('ファイル名', render_kw={"disabled": "disabled"})


class FileForm(FlaskForm):
    attachment_id = IntegerField('添付id')
    upload = FileField("アップロードファイル", validators=[FileAllowed(files)], filters=[lambda x: x or None])

    def validate_upload(self, field):
        if self.attachment_id.data is None and (field.data or None) is None:
            raise ValidationError(field.label.text + 'は必須です')

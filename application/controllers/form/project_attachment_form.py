from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SelectField, DateTimeField
from wtforms import ValidationError

from application.controllers.form.fields import IntegerField
from application.controllers.form.validators import DataRequired, Length, FileAllowed
from application.domain.model.immutables.project_attachment_type import ProjectAttachmentType
from application.domain.model.upload_set import UploadSet

files = UploadSet('files', ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'xlsx', 'xls', 'doc', 'docx', 'txt'])


class ProjectAttachmentForm(FlaskForm):
    id = IntegerField('id')
    project_id = IntegerField('プロジェクトid')
    type = SelectField('添付種類（必須）',
                       [DataRequired()],
                       choices=ProjectAttachmentType.get_type_for_select(),
                       render_kw={"title": "添付種類（必須）"})
    remarks = StringField('備考', [Length(max=256)])
    filename = StringField('ファイル名', render_kw={"disabled": "disabled"})
    updated_user = StringField('更新者')
    updated_at = DateTimeField('更新日')


class FileForm(FlaskForm):
    attachment_id = IntegerField('添付id')
    upload = FileField("アップロードファイル（必須）", validators=[FileAllowed(files)], filters=[lambda x: x or None])

    def validate_upload(self, field):
        if self.attachment_id.data is None and (field.data or None) is None:
            raise ValidationError(field.label.text + 'は必須です')

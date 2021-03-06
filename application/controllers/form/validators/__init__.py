from datetime import date

from flask_wtf import file
from wtforms import ValidationError
from wtforms import validators
from wtforms.compat import string_types
from wtforms.validators import StopValidation


class Length(validators.Length):
    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            message = self.message
            if message is None:
                if self.max == -1:
                    message = field.ngettext('%(min)d 文字以上の入力が必要です',
                                             '%(min)d 文字以上の入力が必要です', self.min)
                elif self.min == -1:
                    message = field.ngettext('%(max)d 文字以内で入力してください',
                                             '%(max)d 文字以内で入力してください', self.max)
                else:
                    message = field.gettext('%(min)d 文字以上、%(max)d 文字以内で入力してください')

            raise ValidationError(message % dict(min=self.min, max=self.max, length=l))


class DataRequired(validators.DataRequired):
    def __call__(self, form, field):
        if not field.data or isinstance(field.data, string_types) and not field.data.strip():
            if self.message is None:
                message = field.gettext('{}は必須です'.format(field.label.text))
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)


class InputRequired(validators.InputRequired):
    def __call__(self, form, field):
        if not field.raw_data or not field.raw_data[0]:
            if self.message is None:
                message = field.gettext('{}は必須です'.format(field.label.text))
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)


class FileAllowed(file.FileAllowed):
    def __call__(self, form, field):
        if not field.has_file():
            return

        filename = field.data.filename.lower()

        if isinstance(self.upload_set, (tuple, list)):
            if any(filename.endswith('.' + x) for x in self.upload_set):
                return
            message = (
                'この拡張子のファイルは保存できません: {}'
            ).format(self.upload_set)
            raise StopValidation(self.message or message)

        if not self.upload_set.file_allowed(field.data, filename):
            raise StopValidation(self.message or
                                 'この拡張子のファイルは保存できません')


class LessThan(object):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("フィールド名 '%s' が見つかりません。") % self.fieldname)
        if field.data and other.data and field.data > other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                if isinstance(field.data, date):
                    message = field.gettext('{} は %(other_label)sより前の日付にして下さい。'.format(field.label.text))
                else:
                    message = field.gettext('{} は %(other_label)sより小さい値にして下さい。'.format(field.label.text))

            raise ValidationError(message % d)


class NumberRange(validators.NumberRange):
    def __call__(self, form, field):
        data = field.data
        if data is not None and \
            ((self.min is not None and data < self.min) or (self.max is not None and data > self.max)):
            message = self.message
            if message is None:
                if self.min is not None and data < self.min:
                    message = field.gettext('%(min)s 以上の数値を入力して下さい。')
                else:
                    message = field.gettext('%(max)s 以下の数値を入力して下さい。')

            raise ValidationError(message % dict(min=self.min, max=self.max))

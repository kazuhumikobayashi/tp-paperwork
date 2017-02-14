import decimal
from datetime import datetime

from wtforms import IntegerField, DecimalField, DateField


class IntegerField(IntegerField):

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '':
                self.data = None
            else:
                try:
                    self.data = int(valuelist[0])
                except ValueError:
                    raise ValueError(self.gettext('{}は数値で入力してください'.format(self.label.text)))


class DecimalField(DecimalField):

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '':
                self.data = None
            else:
                try:
                    if self.use_locale:
                        self.data = self._parse_decimal(valuelist[0])
                    else:
                        self.data = decimal.Decimal(valuelist[0])
                except (decimal.InvalidOperation, ValueError):
                    raise ValueError(self.gettext('{}は数値で入力してください'.format(self.label.text)))


class DateField(DateField):

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.strptime(date_str, self.format).date()
            except ValueError:
                raise ValueError(self.gettext('{}はyyyy/mm/dd形式で入力してください'.format(self.label.text)))

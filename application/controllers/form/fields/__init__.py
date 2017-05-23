import decimal
import time
from datetime import datetime, timedelta, date

import wtforms


class IntegerField(wtforms.IntegerField):

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '':
                self.data = None
            else:
                try:
                    self.data = int(valuelist[0])
                except ValueError:
                    raise ValueError(self.gettext('{}は数値で入力してください'.format(self.label.text)))


class DecimalField(wtforms.DecimalField):

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


class DateField(wtforms.DateField):

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.strptime(date_str, self.format).date()
            except ValueError:
                raise ValueError(self.gettext('{}はyyyy/mm/dd形式で入力してください'.format(self.label.text)))


class BeginningOfMonthField(wtforms.DateField):

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                tmp_data = datetime.strptime(date_str, self.format).date()
                self.data = date(tmp_data.year, tmp_data.month, 1)
            except ValueError:
                raise ValueError(self.gettext('{}はyyyy/mm形式で入力してください'.format(self.label.text)))


class EndOfMonthField(wtforms.DateField):

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                tmp_data = datetime.strptime(date_str, self.format).date()
                self.data = date.fromtimestamp(time.mktime((tmp_data.year, tmp_data.month + 1, 1, 0, 0, 0, 0, 0, 0))) - timedelta(days=1)
            except ValueError:
                raise ValueError(self.gettext('{}はyyyy/mm形式で入力してください'.format(self.label.text)))

import decimal
from datetime import datetime, date

import wtforms
from dateutil.relativedelta import relativedelta
from wtforms import widgets

from application.controllers.form.widgets import SelectWithDisable


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
            if date_str == '':
                self.data = None
            else:
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
                d = datetime.strptime(date_str, self.format).date()
                self.data = d + relativedelta(months=1, days=-1)
            except ValueError:
                raise ValueError(self.gettext('{}はyyyy/mm形式で入力してください'.format(self.label.text)))


class RadioField(wtforms.RadioField):
    
    def process_data(self, value):
        try:
            if value:
                self.data = self.coerce(value)
            else:
                self.data = None
        except (ValueError, TypeError):
            self.data = None
            
    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == v or self.data is None:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class CheckboxField(wtforms.SelectMultipleField):
    """
    Like a SelectField, except displays a list of radio buttons.

    Iterating the field will produce subfields (each containing a label as
    well) in order to allow custom rendering of the individual radio fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SelectMultipleFieldWithDisable(wtforms.SelectField):
    widget = SelectWithDisable()

    def iter_choices(self):
        for value, label, disabled in self.choices:
            selected = self.data is not None and self.coerce(value) in self.data
            yield (value, label, selected, disabled)

    def pre_validate(self, form):
        for v, _, _ in self.choices:
            if self.data == v:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))

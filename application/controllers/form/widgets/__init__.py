from html import escape

from requests.packages.idna import unicode
from wtforms import widgets


class SelectWithDisable(object):
    """
    Renders a select field.

    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected, disabled)`.
    """
    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = 'multiple'
            kwargs['size'] = len(field.choices) if len(field.choices) < 15 else 15
        html = ['<select %s>' % widgets.html_params(name=field.name, **kwargs)]
        for val, label, selected, disabled in field.iter_choices():
            html.append(self.render_option(val, label, selected, disabled))
        html.append('</select>')
        return widgets.HTMLString(u''.join(html))

    @classmethod
    def render_option(cls, value, label, selected, disabled):
        options = {'value': value}
        if selected:
            options['selected'] = 'selected'
        if disabled:
            options['disabled'] = 'disabled'
        return widgets.HTMLString('<option %s>%s</option>' % (widgets.html_params(**options), escape(unicode(label))))


class SelectWithSubtext(object):
    """
    Renders a select field.

    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected, subtext)`.
    """
    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = 'multiple'
            kwargs['size'] = len(field.choices) if len(field.choices) < 15 else 15
        html = ['<select %s>' % widgets.html_params(name=field.name, **kwargs)]
        for val, label, selected, subtext in field.iter_choices():
            html.append(self.render_option(val, label, selected, subtext))
        html.append('</select>')
        return widgets.HTMLString(''.join(html))

    @classmethod
    def render_option(cls, value, label, selected, subtext):
        options = {'value': value}
        if selected:
            options['selected'] = 'selected'
        if subtext:
            options['data-subtext'] = subtext
        return widgets.HTMLString('<option %s>%s</option>' % (widgets.html_params(**options), escape(unicode(label))))

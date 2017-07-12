from flask import session


class PageSessionService(object):

    def __init__(self, page):
        self.page = page
        if session.get('pre_page'):
            pre_page = session.get('pre_page')
            if pre_page != self.page:
                session.pop('pre_page', None)

    def save(self):
        if self.page:
            session['pre_page'] = self.page
        return self

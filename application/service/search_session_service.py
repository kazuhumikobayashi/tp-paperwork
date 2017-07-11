import pickle

from flask import session
from werkzeug.datastructures import ImmutableMultiDict

from application.domain.model.form.search import Search


class SearchSessionService(object):

    def __init__(self, page, request_args=None):
        self.search = Search(page, request_args)
        if session.get('search'):
            search = pickle.loads(session.get('search'))
            if search.page != self.search.page:
                session.pop('search', None)

    def save(self):
        if self.search.request_args:
            session['search'] = pickle.dumps(self.search)
        return self

    def get_dict(self):
        if session.get('search'):
            search = pickle.loads(session.get('search'))
            if search.page == self.search.page:
                return ImmutableMultiDict(search.request_args)
        return None

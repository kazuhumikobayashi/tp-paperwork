from datetime import datetime

from flask import current_app
from flask import session

from application import db
from application.domain.model.base_model import BaseModel


class BaseRepository(object):

    model = BaseModel

    def find_all(self, page=None):
        if page:
            return self.model.query.paginate(page, self.model.PER_PAGE)
        else:
            return self.model.query.all()

    def find_by_id(self, id):
        ret = self.model.query.filter(self.model.id == id).first()
        if ret is None:
            ret = self.create()
        return ret

    def save(self, model):
        if model.id is None:
            model.created_at = datetime.today()
            model.created_user = session['user']['user_name']
        model.updated_at = datetime.today()
        model.updated_user = session['user']['user_name']

        db.session.add(model)
        db.session.commit()
        current_app.logger.debug('save:' + str(model))

    def destroy(self, model):
        db.session.delete(model)
        db.session.commit()
        current_app.logger.debug('destroy:' + str(model))

    def create(self):
        raise Exception("createメソッドを実装して下さい。")

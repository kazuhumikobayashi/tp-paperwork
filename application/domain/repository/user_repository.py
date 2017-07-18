from datetime import datetime

from dateutil.tz import tz
from flask import current_app
from flask import session

from application import db, bcrypt
from application.domain.model.user import User
from application.domain.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):

    model = User

    def find(self, page, user_name, shain_number):
        query = self.model.query
        if user_name:
            query = query.filter(self.model.user_name.like('%' + user_name + '%'))
        if shain_number:
            query = query.filter(self.model.shain_number.like('%' + shain_number + '%'))
        pagination = query.order_by(self.model.shain_number.asc()).paginate(page, self.model.PER_PAGE)
        return pagination

    def find_by_shain_number(self, shain_number):
        return User.query.filter(self.model.shain_number == shain_number).first()

    def save(self, user):
        jst = tz.gettz('Asia/Tokyo')
        now = datetime.now(jst)
        if user.id is None:
            user.created_at = now
            user.created_user = session['user']['user_name']
            user.password = bcrypt.generate_password_hash(user.shain_number)
        user.updated_at = now
        user.updated_user = session['user']['user_name']

        db.session.add(user)
        db.session.commit()
        current_app.logger.debug('save:' + str(user))

    def create(self):
        return User()

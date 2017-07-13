from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import session

from application import bcrypt
from application.controllers.form.pwchange_form import PwChangeForm
from application.domain.model.immutables.message import Message
from application.service.user_service import UserService

bp = Blueprint('pwchange', __name__)
service = UserService()


@bp.route('/pwchange', methods=['GET', 'POST'])
def pwchange():
    form = PwChangeForm(request.form)

    # パスワード変更処理
    if form.validate_on_submit():
        user = service.find_by_id(session['user']['id'])
        if user is not None:
            user.password = bcrypt.generate_password_hash(form.new_password.data)
            service.save(user)
        flash(Message.saved.value)
    # パスワード変更ページを表示する
    return render_template('pwchange/pwchange.html', form=form)

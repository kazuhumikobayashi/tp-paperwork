from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.user_form import UserForm
from application.service.user_service import UserService

bp = Blueprint('user', __name__, url_prefix='/user')
service = UserService()


@bp.route('/', methods=['GET'])
def index(page=1):
    user_name = request.args.get('user_name','')
    shain_number = request.args.get('shain_number','')
    pagination = service.find(page, user_name, shain_number)
    return render_template('user/index.html', pagination=pagination)


@bp.route('/page/<int:page>', methods=['GET'])
def user_page(page=1):
    return index(page)


@bp.route('/detail/<user_id>', methods=['GET', 'POST'])
def detail(user_id=None):
    user = service.find_by_id(user_id)
    current_app.logger.debug(str(user))

    if user.id is None and user_id is not None:
        return abort(404)
    form = UserForm(request.form, user)

    if form.validate_on_submit():
        user.shain_number = form.shain_number.data
        user.user_name = form.user_name.data
        user.mail = form.mail.data

        service.save(user)
        flash('保存しました。')
        return redirect(url_for('.detail', user_id=user.id))
    return render_template('user/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<user_id>', methods=['GET'])
def delete(user_id):
    user = service.find_by_id(user_id)
    if user.id is not None:
        service.destroy(user)
        flash('削除しました。')
    return redirect('/user')

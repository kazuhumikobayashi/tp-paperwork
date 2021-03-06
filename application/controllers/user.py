from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.user_form import UserForm
from application.controllers.form.user_search_form import UserSearchForm
from application.domain.model.immutables.message import Message
from application.service.search_session_service import SearchSessionService
from application.service.user_service import UserService

bp = Blueprint('user', __name__, url_prefix='/user')
service = UserService()


@bp.route('/', methods=['GET'])
def index(page=1):
    search = SearchSessionService('user', request.args)
    search.save()
    form = UserSearchForm(search.get_dict())
    pagination = service.find(page, form.user_name.data, form.shain_number.data)
    return render_template('master/user/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def user_page(page=1):
    return index(page)


@bp.route('/detail/<user_id>', methods=['GET', 'POST'])
def detail(user_id=None):
    user = service.find_by_id(user_id)

    if user.id is None and user_id is not None:
        return abort(404)
    form = UserForm(request.form, obj=user)
    
    if user.id:
        form.shain_number.render_kw = {"disabled": "disabled"}
        form.shain_number.data = user.shain_number

    if form.validate_on_submit():
        user.shain_number = form.shain_number.data
        user.user_name = form.user_name.data

        service.save(user)
        flash(Message.saved.value)
        return redirect(url_for('.detail', user_id=user.id))
    current_app.logger.debug(form.errors)
    if form.errors:
        flash(Message.saving_failed.value, 'error')
    return render_template('master/user/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<user_id>', methods=['GET'])
def delete(user_id):
    user = service.find_by_id(user_id)
    if user.id is not None:
        service.destroy(user)
        flash(Message.deleted.value)
    return redirect('/user')

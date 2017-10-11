from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.bank_form import BankForm
from application.controllers.form.bank_search_form import BankSearchForm
from application.domain.model.immutables.message import Message
from application.service.bank_service import BankService
from application.service.search_session_service import SearchSessionService

bp = Blueprint('bank', __name__, url_prefix='/bank')
service = BankService()


@bp.route('/', methods=['GET'])
def index(page=1):
    search = SearchSessionService('bank', request.args)
    search.save()
    form = BankSearchForm(search.get_dict())
    pagination = service.find(page, form.bank_name.data, form.text_for_document.data)
    return render_template('master/bank/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def bank_page(page=1):
    return index(page)


@bp.route('/detail/<bank_id>', methods=['GET', 'POST'])
def detail(bank_id=None):
    bank = service.find_by_id(bank_id)

    if bank.id is None and bank_id is not None:
        return abort(404)
    form = BankForm(request.form, bank)

    if form.validate_on_submit():
        bank.bank_name = form.bank_name.data
        bank.text_for_document = form.text_for_document.data

        service.save(bank)
        flash(Message.saved.value)
        return redirect(url_for('.detail', bank_id=bank.id))
    current_app.logger.debug(form.errors)
    if form.errors:
        flash(Message.saving_failed.value, 'error')
    return render_template('master/bank/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<bank_id>', methods=['GET'])
def delete(bank_id):
    bank = service.find_by_id(bank_id)
    if bank.id is not None:
        service.destroy(bank)
        flash(Message.deleted.value)
    return redirect('/bank')

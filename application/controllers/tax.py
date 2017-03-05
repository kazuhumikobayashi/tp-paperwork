from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.tax_form import TaxForm
from application.service.tax_service import TaxService

bp = Blueprint('tax', __name__, url_prefix='/tax')
service = TaxService()


@bp.route('/', methods=['GET'])
def index(page=1):
    tax_rate = request.args.get('tax_rate', '')
    pagination = service.find(page, tax_rate)
    return render_template('tax/index.html', pagination=pagination)


@bp.route('/page/<int:page>', methods=['GET'])
def tax_page(page=1):
    return index(page)


@bp.route('/detail/<tax_id>', methods=['GET', 'POST'])
def detail(tax_id=None):
    tax = service.find_by_id(tax_id)

    if tax.id is None and tax_id is not None:
        return abort(404)
    form = TaxForm(request.form, tax)

    if form.validate_on_submit():
        tax.start_date = form.start_date.data
        tax.end_date = form.end_date.data
        tax.tax_rate = form.tax_rate.data

        service.save(tax)
        flash('保存しました。')
        return redirect(url_for('.detail', tax_id=tax.id))
    current_app.logger.debug(form.errors)
    return render_template('tax/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<tax_id>', methods=['GET'])
def delete(tax_id):
    tax = service.find_by_id(tax_id)
    if tax.id is not None:
        service.destroy(tax)
        flash('削除しました。')
    return redirect('/tax')

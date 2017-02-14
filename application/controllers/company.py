from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.company_form import CompanyForm
from application.service.company_service import CompanyService

bp = Blueprint('company', __name__, url_prefix='/company')
service = CompanyService()


@bp.route('/', methods=['GET', 'POST'])
def index(page=1):
    company_name = request.args.get('company_name','')
    company_code = request.args.get('company_code','')
    pagination = service.find(page, company_name, company_code)
    return render_template('company/index.html', pagination=pagination)


@bp.route('/page/<int:page>', methods=['GET', 'POST'])
def company_page(page=1):
    return index(page)


@bp.route('/detail/<company_id>', methods=['GET', 'POST'])
def detail(company_id=None):
    company = service.find_by_id(company_id)
    current_app.logger.debug(str(company))

    if company is None and company_id is not None:
        return abort(404)
    form = CompanyForm(request.form, company)
    if form.validate_on_submit():
        company.company_code = form.company_code.data
        company.company_name = form.company_name.data
        company.company_name_kana = form.company_name_kana.data
        company.trade_name = form.trade_name.data
        company.trade_name_position = form.trade_name_position.data
        company.client_flg = form.client_flg.data
        company.consignment_flg = form.consignment_flg.data
        company.start_date = form.start_date.data
        company.end_date = form.end_date.data
        company.postal_code = form.postal_code.data
        company.address1 = form.address1.data
        company.address2 = form.address2.data
        company.phone = form.phone.data
        company.fax = form.fax.data
        company.payment_site = form.payment_site.data
        company.receipt_site = form.receipt_site.data
        company.tax = form.tax.data
        company.remarks = form.remarks.data

        service.save(company)
        flash('保存しました。')
        return redirect(url_for('.detail', company_id=company.id))
    return render_template('company/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<company_id>', methods=['GET'])
def delete(company_id):
    company = service.find_by_id(company_id)
    if company is not None:
        service.destroy(company)
        flash('削除しました。')
    return redirect('/company')

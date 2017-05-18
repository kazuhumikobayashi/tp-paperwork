from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from wtforms import validators

from application.const import ClientFlag
from application.controllers.form.company_form import CompanyForm
from application.controllers.form.company_search_form import CompanySearchForm
from application.domain.model.company_client_flag import CompanyClientFlag
from application.service.bank_service import BankService
from application.service.client_flag_service import ClientFlagService
from application.service.company_service import CompanyService


bp = Blueprint('company', __name__, url_prefix='/company')
service = CompanyService()
bank_service = BankService()
client_flag_service = ClientFlagService()


@bp.route('/', methods=['GET'])
def index(page=1):
    form = CompanySearchForm(request.values)
    form.client_flag_id.choices = client_flag_service.find_all_for_multi_select()
    form.bank_id.choices = bank_service.find_all_for_multi_select()

    pagination = service.find(page, form.company_name.data, form.client_flag_id.data,
                              form.bank_id.data)
    return render_template('company/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def company_page(page=1):
    return index(page)


@bp.route('/detail/<company_id>', methods=['GET', 'POST'])
def detail(company_id=None):
    company = service.find_by_id(company_id)
    current_app.logger.debug(str(company))

    if company.id is None and company_id is not None:
        return abort(404)
    company.client_flag = [h.client_flag_id for h in company.company_client_flags]
    form = CompanyForm(request.form, company)
    form.bank_id.choices = bank_service.find_all_for_select()
    form.client_flag.choices = client_flag_service.find_all_for_multi_select()
    
    if form.validate_on_submit():
        company.company_name = form.company_name.data
        company.company_name_kana = form.company_name_kana.data
        company.company_short_name = form.company_short_name.data
        company.contract_date = form.contract_date.data
        company.postal_code = form.postal_code.data
        company.address = form.address.data
        company.phone = form.phone.data
        company.fax = form.fax.data
        company.client_code = form.client_code.data
        company.bp_code = form.bp_code.data
        company.payment_site = form.payment_site.data or None
        company.receipt_site = form.receipt_site.data or None
        company.payment_tax = form.payment_tax.data or None
        company.receipt_tax = form.receipt_tax.data or None
        company.bank_id = form.bank_id.data or None
        company.bank_holiday_flag = form.bank_holiday_flag.data
        company.remarks = form.remarks.data
        company.print_name = form.print_name.data
        client_flags = []
        for client_flag_id in form.client_flag.data:
            client_flags.extend([CompanyClientFlag(company.id, client_flag_id)])
        company.company_client_flags = client_flags

        service.save(company)
        flash('保存しました。')
        return redirect(url_for('.detail', company_id=company.id))
    current_app.logger.debug(form.errors)
    return render_template('company/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<company_id>', methods=['GET'])
def delete(company_id):
    company = service.find_by_id(company_id)
    if company.id is not None:
        service.destroy(company)
        flash('削除しました。')
    return redirect('/company')

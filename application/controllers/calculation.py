from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.const import FORMULA
from application.controllers.form.calculation_form import CalculationForm
from application.service.calculation_service import CalculationService

bp = Blueprint('calculation', __name__, url_prefix='/calculation')
service = CalculationService()


@bp.route('/', methods=['GET'])
def index(page=1):
    calculation_name = request.args.get('calculation_name', '')
    pagination = service.find(page, calculation_name)
    return render_template('calculation/index.html', pagination=pagination)


@bp.route('/page/<int:page>', methods=['GET'])
def calculation_page(page=1):
    return index(page)


@bp.route('/detail/<calculation_id>', methods=['GET', 'POST'])
def detail(calculation_id=None):
    calculation = service.find_by_id(calculation_id)

    if calculation.id is None and calculation_id is not None:
        return abort(404)
    form = CalculationForm(request.form, calculation)

    if form.validate_on_submit():
        calculation_name = None

        for formula in FORMULA:
            if formula[0] == form.formula.data:
                calculation_name = formula[1]
                break

        calculation.calculation_name = str(form.amount.data) + '円' + calculation_name
        calculation.amount = form.amount.data
        calculation.formula = form.formula.data

        service.save(calculation)
        flash('保存しました。')
        return redirect(url_for('.detail', calculation_id=calculation.id))
    return render_template('calculation/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<calculation_id>', methods=['GET'])
def delete(calculation_id):
    calculation = service.find_by_id(calculation_id)
    if calculation.id is not None:
        service.destroy(calculation)
        flash('削除しました。')
    return redirect('/calculation')

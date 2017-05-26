from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.engineer_history_form import EngineerHistoryForm
from application.service.business_category_service import BusinessCategoryService
from application.service.company_service import CompanyService
from application.service.engineer_history_service import EngineerHistoryService
from application.service.engineer_service import EngineerService
from application.service.skill_service import SkillService


bp = Blueprint('engineer_history', __name__, url_prefix='/engineer_history')
service = EngineerService()
engineer_history_service = EngineerHistoryService()
company_service = CompanyService()
skill_service = SkillService()
business_category_service = BusinessCategoryService()


@bp.route('/<engineer_history_id>', methods=['GET', 'POST'])
def history(engineer_history_id=None):
    engineer_id = request.args.get('engineer_id')
    engineer_history = engineer_history_service.find_by_id(engineer_history_id)

    if engineer_history.id is None and engineer_history_id is not None:
        return abort(404)
    form = EngineerHistoryForm(request.form, engineer_history)

    # 履歴データ新規作成時にはengineer情報を取得する。
    if engineer_id:
        engineer_history.engineer = service.find_by_id(engineer_id)

    form.receipt_site.data = engineer_history.engineer.company.receipt_site
    form.receipt_tax.data = str(engineer_history.engineer.company.receipt_tax)

    # 対象技術者の最新の履歴データを取得する
    latest_engineer_history = engineer_history_service.get_latest_history(engineer_history.engineer.id)

    if form.validate_on_submit():
        # 支払い契約開始年月のデータに変更があった場合、履歴を切る。
        if engineer_history.receipt_start_day != form.receipt_start_day.data:
            engineer_history = engineer_history.create_new_history()
        engineer_history.engineer_id = engineer_history.engineer.id
        engineer_history.receipt_start_day = form.receipt_start_day.data
        engineer_history.receipt_end_day = form.receipt_end_day.data
        engineer_history.receipt_per_month = form.receipt_per_month.data
        engineer_history.receipt_rule = form.receipt_rule.data
        engineer_history.receipt_bottom_base_hour = form.receipt_bottom_base_hour.data
        engineer_history.receipt_top_base_hour = form.receipt_top_base_hour.data
        engineer_history.receipt_free_base_hour = form.receipt_free_base_hour.data
        engineer_history.receipt_per_hour = form.receipt_per_hour.data
        engineer_history.receipt_per_bottom_hour = form.receipt_per_bottom_hour.data
        engineer_history.receipt_per_top_hour = form.receipt_per_top_hour.data
        engineer_history.receipt_fraction = form.receipt_fraction.data
        engineer_history.receipt_fraction_calculation1 = form.receipt_fraction_calculation1.data
        engineer_history.receipt_fraction_calculation2 = form.receipt_fraction_calculation2.data
        engineer_history.receipt_condition = form.receipt_condition.data
        engineer_history.remarks = form.remarks.data

        engineer_history_service.save(engineer_history)
        flash('保存しました。')
        return redirect(url_for('.history', engineer_history_id=engineer_history.id))
    current_app.logger.debug(form.errors)
    return render_template('engineer/history.html',
                           form=form,
                           engineer_id=engineer_history.engineer.id,
                           latest_engineer_history=latest_engineer_history)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return history()


@bp.route('/delete/<engineer_history_id>', methods=['GET'])
def delete(engineer_history_id):
    engineer_history = engineer_history_service.find_by_id(engineer_history_id)
    engineer_id = engineer_history.engineer_id
    if engineer_history.id is not None:
        engineer_history_service.destroy(engineer_history)
        flash('削除しました。')
    return redirect('/engineer/detail/' + str(engineer_id))

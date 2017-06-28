from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.engineer_form import EngineerForm
from application.controllers.form.engineer_search_form import EngineerSearchForm
from application.domain.model.engineer_business_category import EngineerBusinessCategory
from application.domain.model.engineer_skill import EngineerSkill
from application.domain.model.immutables.client_flag import ClientFlag
from application.domain.model.immutables.gender import Gender
from application.service.business_category_service import BusinessCategoryService
from application.service.company_service import CompanyService
from application.service.engineer_history_service import EngineerHistoryService
from application.service.engineer_service import EngineerService
from application.service.skill_service import SkillService

bp = Blueprint('engineer', __name__, url_prefix='/engineer')
service = EngineerService()
engineer_history_service = EngineerHistoryService()
company_service = CompanyService()
skill_service = SkillService()
business_category_service = BusinessCategoryService()


@bp.route('/', methods=['GET'])
def index(page=1):
    form = EngineerSearchForm(request.values)
    form.company_id.choices = company_service.find_for_multi_select_by_client_flag_id(
        [ClientFlag.our_company.value, ClientFlag.bp.value])
    form.skill_id.choices = skill_service.find_all_for_multi_select()
    form.business_category_id.choices = business_category_service.find_all_for_multi_select()

    pagination = service.find(page,
                              form.engineer_name.data,
                              form.company_id.data,
                              form.contract_engineer_is_checked.data,
                              form.skill_id.data,
                              form.business_category_id.data)
    return render_template('master/engineer/index.html',
                           pagination=pagination,
                           form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def engineer_page(page=1):
    return index(page)


@bp.route('/detail/<engineer_id>', methods=['GET', 'POST'])
def detail(engineer_id=None):
    engineer = service.find_by_id(engineer_id)

    if engineer.id is None and engineer_id is not None:
        return abort(404)
    engineer.skill = [h.skill_id for h in engineer.engineer_skills]
    engineer.business_category = [
        h.business_category_id for h in engineer.engineer_business_categories]
    form = EngineerForm(request.form, engineer)
    form.company_id.choices = company_service.find_for_select_by_client_flag_id(
        [ClientFlag.our_company.value, ClientFlag.bp.value])
    form.skill.choices = skill_service.find_all_for_multi_select()
    form.business_category.choices = business_category_service.find_all_for_multi_select()

    # 更新時、所属会社を変更不可。
    if engineer.id:
        form.company_id.render_kw = {"disabled": "disabled"}

    if form.validate_on_submit():
        engineer.engineer_name = form.engineer_name.data
        engineer.engineer_name_kana = form.engineer_name_kana.data
        engineer.birthday = form.birthday.data
        engineer.gender = Gender.parse(form.gender.data)
        if engineer.id is None:
            engineer.company_id = form.company_id.data
        skills = []
        for skill_id in form.skill.data:
            skills.extend([EngineerSkill(engineer.id, skill_id)])
        engineer.engineer_skills = skills
        business_categories = []
        for business_category_id in form.business_category.data:
            business_categories.extend(
                [EngineerBusinessCategory(engineer.id, business_category_id)])
        engineer.engineer_business_categories = business_categories

        service.save(engineer)
        flash('保存しました。')
        return redirect(url_for('.detail', engineer_id=engineer.id))

    engineer_histories = engineer_history_service.find_by_engineer_id(
        engineer.id)
    # 最新の履歴データ取得
    latest_engineer_history = engineer_history_service.get_latest_history(
        engineer.id)
    current_app.logger.debug(form.errors)
    return render_template('master/engineer/detail.html',
                           form=form,
                           engineer_histories=engineer_histories,
                           latest_engineer_history=latest_engineer_history)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<engineer_id>', methods=['GET'])
def delete(engineer_id):
    engineer = service.find_by_id(engineer_id)
    if engineer.id is not None:
        service.destroy(engineer)
        flash('削除しました。')
    return redirect('/engineer')

from flask import Blueprint
from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from application.controllers.form.business_category_form import BusinessCategoryForm
from application.service.business_category_service import BusinessCategoryService

bp = Blueprint('business_category', __name__, url_prefix='/business_category')
service = BusinessCategoryService()


@bp.route('/', methods=['GET'])
def index(page=1):
    business_category_name = request.args.get('business_category_name', '')
    pagination = service.find(page, business_category_name)
    return render_template('business_category/index.html', pagination=pagination)


@bp.route('/page/<int:page>', methods=['GET'])
def business_category_page(page=1):
    return index(page)


@bp.route('/detail/<business_category_id>', methods=['GET', 'POST'])
def detail(business_category_id=None):
    business_category = service.find_by_id(business_category_id)

    if business_category.id is None and business_category_id is not None:
        return abort(404)
    form = BusinessCategoryForm(request.form, business_category)

    if form.validate_on_submit():
        business_category.business_category_name = form.business_category_name.data

        service.save(business_category)
        flash('保存しました。')
        return redirect(url_for('.detail', business_category_id=business_category.id))
    return render_template('business_category/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<business_category_id>', methods=['GET'])
def delete(business_category_id):
    business_category = service.find_by_id(business_category_id)
    if business_category.id is not None:
        service.destroy(business_category)
        flash('削除しました。')
    return redirect('/business_category')

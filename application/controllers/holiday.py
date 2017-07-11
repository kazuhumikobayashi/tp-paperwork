from datetime import datetime

from flask import Blueprint
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from httplib2 import ServerNotFoundError

from application.controllers.form.holiday_form import HolidayForm
from application.controllers.form.holiday_search_form import HolidaySearchForm
from application.service.calendar_service import CalendarService
from application.service.holiday_service import HolidayService
from application.service.search_session_service import SearchSessionService

bp = Blueprint('holiday', __name__, url_prefix='/holiday')
service = HolidayService()
calendar_service = CalendarService()


@bp.route('/', methods=['GET'])
def index(page=1):
    search = SearchSessionService('holiday', request.args)
    search.save()
    form = HolidaySearchForm(search.get_dict())
    _save_holidays_when_no_data()

    pagination = service.find_by_year(form.year.data, page)
    return render_template('master/holiday/index.html', pagination=pagination, form=form)


@bp.route('/page/<int:page>', methods=['GET'])
def holiday_page(page=1):
    return index(page)


@bp.route('/detail/<holiday_id>', methods=['GET', 'POST'])
def detail(holiday_id=None):
    holiday = service.find_by_id(holiday_id)

    if holiday.id is None and holiday_id is not None:
        return abort(404)
    form = HolidayForm(request.form, holiday)

    if form.validate_on_submit():
        holiday.holiday = form.holiday.data
        holiday.holiday_name = form.holiday_name.data

        service.save(holiday)
        flash('保存しました。')
        return redirect(url_for('.detail', holiday_id=holiday.id))
    current_app.logger.debug(form.errors)
    return render_template('master/holiday/detail.html', form=form)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    return detail()


@bp.route('/delete/<holiday_id>', methods=['GET'])
def delete(holiday_id):
    holiday = service.find_by_id(holiday_id)
    if holiday.id is not None:
        service.destroy(holiday)
        flash('削除しました。')
    return redirect('/holiday')


def _save_holidays_when_no_data():
    this_year = datetime.today().year
    for offset in [-1, 0, 1]:
        year = this_year + offset
        holidays = service.find_by_year(str(year))
        if not holidays:
            try:
                holidays = calendar_service.find_holiday_by_year(year)
                service.save(holidays)
            except ServerNotFoundError:
                pass

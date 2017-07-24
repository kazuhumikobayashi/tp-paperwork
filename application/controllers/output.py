from flask import Blueprint
from flask import current_app
from flask import request
from flask import render_template

from application.controllers.form.output_form import OutputForm

bp = Blueprint('output', __name__, url_prefix='/output')


@bp.route('/', methods=['GET', 'POST'])
def detail():
    form = OutputForm(request.form)

    current_app.logger.debug(form.errors)
    return render_template('output/download.html', form=form)

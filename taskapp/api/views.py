from flask import Blueprint, render_template, current_app
from flask.ext.login import current_user, login_required
from . import forms
from taskapp.models import User, Devices, Entries
from taskapp.extensions import db


blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')


@blueprint.route('/upload')
@blueprint.route('/upload/<problem_id>')
@login_required
def api_upload(problem_id=None):
    """Create an embeddable form that will redirect to '/upload'"""
    form = forms.make_upload_form(problem_id)
    return render_template('api/upload.html', form=form)


@blueprint.route('/entries')
@blueprint.route('/entries/<device_num>')
@blueprint.route('/entries/<device_num>/<int:page_num>')
@login_required
def entries(device_num=None, page_num=1):
    entr1 = Entries.query.filter(Entries.user_id == current_user.id).order_by(Entries.entry_id.desc())
    if device_num is not None:
        entr = entr1.filter(Entries.device_num == device_num).order_by(Entries.entry_id.desc())
        entr = entr.paginate(page_num,current_app.config['MAX_ENTRIES_PER_PAGE'], False)
    else:
        entr = None

    all_entries = entr1.filter(Entries.device_num == device_num).order_by(Entries.time_stamp.asc()).all()


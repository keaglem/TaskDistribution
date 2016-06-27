from flask import Blueprint, render_template, current_app
from flask.ext.login import current_user, login_required
from . import forms
from taskapp.models import Submission
from taskapp.extensions import db


blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')


@blueprint.route('/upload')
@blueprint.route('/upload/<problem_id>')
@login_required
def api_upload(problem_id=None):
    """Create an embeddable form that will redirect to '/upload'"""
    form = forms.make_upload_form(problem_id)
    return render_template('api/upload.html', form=form)


@blueprint.route('/submissions')
@blueprint.route('/submissions/<sub_num>')
@blueprint.route('/submissions/<sub_num>/<int:page_num>')
@login_required
def entries(sub_num=None, page_num=1):
    sub1 = Submission.query.filter(Submission.user_id == current_user.id).order_by(Submission.sub_id.desc())
    if sub_num is not None:
        sub = entr1.filter(Entries.device_num == device_num).order_by(Entries.entry_id.desc())
        sub = entr.paginate(page_num, current_app.config['MAX_ENTRIES_PER_PAGE'], False)
    else:
        sub = Submission.query.all()

    all_entries = sub1.filter(Submission.device_num == sub_num).order_by(Submission.submission_time.asc()).all()


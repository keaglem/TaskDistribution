from flask import Blueprint, render_template, current_app, jsonify, request, abort
from flask.ext.login import current_user, login_required
from . import forms
from taskapp.models import Submission, Simulation
from taskapp.extensions import db_session


blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')


@blueprint.route('/upload')
@blueprint.route('/upload/<problem_id>')
@login_required
def api_upload(problem_id=None):
    """Create an embeddable form that will redirect to '/upload'"""
    form = forms.make_upload_form(problem_id)
    return render_template('api/upload.html', form=form)


@blueprint.route('/simulations/')
@blueprint.route('/simulations/<sim_num>')
@blueprint.route('/simulations/<sim_num>/<int:page_num>')
@login_required
def simulations(sim_num=None, page_num=1):
    """Return the simulations for a given user, optionally filtered by submission id"""
    sim1 = Simulation.query.filter(Simulation.user_id == current_user.id).order_by(Simulation.simulation_id.desc())
    if sim_num is not None:
        sim = sim1.filter(Simulation.simulation_id == sim_num).order_by(Simulation.simulation_id.desc())
        sim = sim.paginate(page_num, current_app.config['MAX_ENTRIES_PER_PAGE'], False)
    else:
        sim = Simulation.query.all()

    simulations = sim.filter(Simulation.simulation_id == sim_num).order_by(Simulation.simulation_id.asc()).all()

    return render_template('api/simulations.html', simlations=sim)


@blueprint.route('/submissions')
@blueprint.route('/submissions/<sub_num>')
@blueprint.route('/submissions/<sub_num>/<int:page_num>')
@login_required
def submissions(sub_num=None, page_num=1):
    """Return the submissions for a given user, optionally filtered by submission id"""
    sub1 = Submission.query.filter(Submission.user_id == current_user.id).order_by(Submission.sub_id.desc())
    if sub_num is not None:
        sub = sub1.filter(Submission.sub_id == sub_num).order_by(Submission.sub_id.desc())
        sub = sub.paginate(page_num, current_app.config['MAX_ENTRIES_PER_PAGE'], False)
    else:
        sub = Submission.query.all()

    all_submissions = sub1.filter(Submission.sub_id == sub_num).order_by(Submission.submission_time.asc()).all()

    return render_template('api/submissions.html', submissions=sub)


@blueprint.route('/get_job')
def get_job():
    sim_val = Simulation.query.filter(Simulation.has_started is False).\
                   order_by(Simulation.simulation_id.asc()).one_or_none()
    return jsonify({'job': sim_val})


@blueprint.route('/add_job')
def add_job():
    new_sim = Simulation(0, 0)
    db_session.add(new_sim)
    db_session.commit()

@blueprint.route('/finish_job', methods=['PUT'])
def finish_job():
    if not request.json or not 'result' in request.json:
        abort(400)
    sim_json = request.json.get('result')
    sim = Simulation.query.get(sim_json['simulation_id'])
    sim.start_time = sim_json['start_time']
    sim.end_time = sim_json['end_time']
    sim.has_error = sim_json['has_error']
    db_session.commit()



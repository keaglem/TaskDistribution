from flask import Blueprint, render_template, url_for, flash, \
    current_app, jsonify, request, abort, redirect
from flask.ext.login import current_user, login_required
from . import forms
from taskapp.models import Submission, Simulation, User
from taskapp.extensions import db_session
import numpy
import datetime


blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')


@blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Create an embeddable form that will redirect to '/upload'"""
    form = forms.UploadForm()
    if form.validate_on_submit():
        new_sub = Submission(current_user.id,
                             form.script_name.data,
                             form.simulation_name.data,
                             form.script_version.data,
                             form.simulation_version.data)
        db_session.add(new_sub)
        db_session.commit()
        #flash('Submission id {} added.'.format(new_sub.sub_id))
        return redirect(url_for('user.submissions'))
    return render_template('api/upload.html', form=form)


@blueprint.route('/simulations/')
@blueprint.route('/simulations/<int:sim_num>')
@blueprint.route('/simulations/<int:sim_num>/<int:page_num>')
@login_required
def simulations(sim_num=None, page_num=1):
    """Return the simulations for a given user, optionally filtered by submission id"""
    sim = Simulation.query.filter(Simulation.user_id == current_user.id).order_by(Simulation.simulation_id.desc())
    if sim_num is not None:
        sim = sim.filter(Simulation.simulation_id == sim_num).order_by(Simulation.simulation_id.desc())

    return render_template('api/simulations.html', simulations=sim)

@blueprint.route('/all_simulations')
def all_simulations():
    """Return the simulations for a given user, optionally filtered by submission id"""
    sim = Simulation.query.order_by(Simulation.simulation_id.desc())

    return render_template('api/simulations.html', simulations=sim)


@blueprint.route('/submissions')
@blueprint.route('/submissions/<sub_num>')
@blueprint.route('/submissions/<sub_num>/<int:page_num>')
@login_required
def submissions(sub_num=None, page_num=1):
    """Return the submissions for a given user, optionally filtered by submission id"""
    sub = Submission.query.filter(Submission.user_id == current_user.id).order_by(Submission.sub_id.desc())
    if sub_num is not None:
        sub = sub.filter(Submission.sub_id == sub_num).order_by(Submission.sub_id.desc())

    return render_template('api/submissions.html', submissions=sub)


@blueprint.route('/get_job')
@blueprint.route('/get_job/<int:node_id>')
def get_job(node_id=0):
    sim_val = Simulation.query.filter(Simulation.has_started == False).\
                   order_by(Simulation.simulation_id.asc()).first()
    if sim_val:
        sim_val.has_started = True
        sim_val.node_id = request.args['id']
        db_session.commit()
        return_val = sim_val.serialize()
    else:
        return_val = None
    return jsonify({'job': return_val})


@blueprint.route('/add_job')
def add_job():
    test_user = User.query.filter(User.name == 'test').one()

    test_sub = Submission.query.filter(Submission.user_id == test_user.id).\
        filter(Submission.high_level_script_name == 'echo').\
        filter(Submission.simulation_name == 'test').first()

    if not test_sub:
        test_sub = Submission(test_user.id, 'echo', 'test', 1, 1)
        db_session.add(test_sub)
        db_session.commit()

    new_sim = Simulation(test_user.id, test_sub.sub_id)
    new_sim.input_settings_filename = ''
    new_sim.output_filename = 'test.txt'
    new_sim.random_seeding = numpy.random.randint(low=0, high=100000)
    db_session.add(new_sim)
    db_session.commit()
    return ''

@blueprint.route('/add_user')
def add_user():
    user = User.query.filter(User.name == 'test').one_or_none()
    if not user:
        new_user = User('test','test@gmail.com','password')
        print('Adding user {}'.format(new_user.name))

        db_session.add(new_user)
        db_session.commit()
    return ''

@blueprint.route('/finish_job', methods=['PUT'])
def finish_job():
    if not request.json or not 'result' in request.json:
        abort(400)
    sim_json = request.json.get('result')
    sim = Simulation.query.get(sim_json['simulation_id'])
    sim.start_time = datetime.datetime(*sim_json['start_time'][0:6])
    sim.end_time = datetime.datetime(*sim_json['end_time'][0:6])
    sim.has_error = sim_json['has_error']
    sim.is_complete = sim_json['is_complete']

    db_session.commit()

    return ''


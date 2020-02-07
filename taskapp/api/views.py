from flask import Blueprint, render_template, url_for, flash, \
    current_app, jsonify, request, abort, redirect
try:
    from flask_login import current_user, login_required
except:
    from flask.ext.login import current_user, login_required
from . import forms
from taskapp.models import Submission, Simulation, User
from taskapp.extensions import db_session
import numpy
import datetime
from flask_socketio import emit
from .. import app
import requests
import os

blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')

@blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Create an embeddable form that will redirect to '/upload'"""
    form = forms.UploadForm()
    if form.validate_on_submit():
        submission_json = {'id': current_user.id,
                           'script_name': form.script_name.data,
                           'simulation_name': form.simulation_name.data,
                           'script_version': form.script_version.data,
                           'simulation_version': form.simulation_version.data,
                           }
        add_submission_url = current_app.config['DATA_API_URL'] + '/submissions'

        response_json = requests.post(add_submission_url, submission_json)
        
        #flash('Submission id {} added.'.format(new_sub.sub_id))
        return redirect(url_for('user.submissions'))
    return render_template('api/upload.html', form=form)


@blueprint.route('/simulations/')
@blueprint.route('/simulations/<int:sub_num>')
@blueprint.route('/simulations/<int:sub_num>/<int:page_num>')
@login_required
def simulations(sub_num=None, page_num=1):
    """Return the simulations for a given user, optionally filtered by submission id"""
    url_appender = '/simulations'
    url_appender += '' if not sub_num else f'/{sub_num}'
    url_appender += '' if not sub_num else f'/{page_num}'

    json_output = requests.get(f"{current_app.config['DATA_API_URL']}" + url_appender).json()

    return render_template('api/simulations.html', simulations=json_output)

@blueprint.route('/all_simulations')
def all_simulations():
    """Return the simulations for a given user, optionally filtered by submission id"""
    url_appender = '/all_simulations'

    json_output = requests.get(f"{current_app.config['DATA_API_URL']}" + url_appender).json()

    return render_template('api/simulations.html', simulations=json_output)

@blueprint.route('/submissions')
@blueprint.route('/submissions/<sub_num>')
@blueprint.route('/submissions/<sub_num>/<int:page_num>')
@login_required
def submissions(sub_num=None, page_num=1):
    """Return the submissions for a given user, optionally filtered by submission id"""
    url_appender = '/submissions'
    url_appender += '' if not sub_num else f'/{sub_num}'
    url_appender += '' if not sub_num else f'/{page_num}'

    json_output = requests.get(f"{current_app.config['DATA_API_URL']}" + url_appender).json()
    return render_template('api/submissions.html', submissions=json_output)


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

    send_active_jobs()
    return jsonify({'job': return_val})


@blueprint.route('/all_jobs')
def all_jobs(node_id=0):
    sim_val = Simulation.query.all()
    return jsonify([sim.serialize() for sim in sim_val])


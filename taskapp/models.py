import datetime
import os

import itsdangerous
from flask import current_app
from flask.ext.login import UserMixin
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from .extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean(), default=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, plaintext_pass):
        self.name = name
        self.email = email
        self.set_password(plaintext_pass)

    def set_password(self, plaintext_pass):
        self.password = generate_password_hash(plaintext_pass)

    def verify_password(self, plaintext_pass):
        return check_password_hash(self.password, plaintext_pass)

    def __repr__(self):
        return "<User '%s'>" % self.name

    def __str__(self):
        return self.name

    @classmethod
    def from_email(cls, email):
        """Return a user object for a given email."""
        return cls.query.filter(User.email == email).first()

    @classmethod
    def from_name_or_email(cls, name_or_email):
        """Return a user object for a given username or email."""
        return cls.query.filter(or_(User.name == name_or_email, User.email == name_or_email)).first()

    @classmethod
    def authenticate(cls, name_or_email, plaintext_pass):
        """Return a User object given valid credentials.

        The login parameter may be either the username or password.
        None is returned on failure.
        """
        user = cls.from_name_or_email(name_or_email)
        if user and user.verify_password(plaintext_pass):
            return user
        return None

    def get_token(self, tag):
        """Return a token that can be used to validate or reset a user.

        The tag is a plain string that is used as a namespace. It must also be
        passed to from_token."""
        serialzer = itsdangerous.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serialzer.dumps(self.id, salt=tag)

    @classmethod
    def from_token(cls, token, tag, max_age=None):
        """Given a token, return the user for that token."""
        serialzer = itsdangerous.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            id = serialzer.loads(token, max_age=max_age, salt=tag)
        except itsdangerous.BadData:
            return None
        return cls.query.get(int(id))


class Simulation(db.Model):
    """


    """
    simulation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    high_level_script_name = db.Column(db.Text(), nullable=False)
    simulation_name = db.Column(db.Text(), nullable=False)
    high_level_script_version = db.Column(db.Integer, nullable=False)
    simulation_version = db.Column(db.Integer, nullable=False)
    random_seeding = db.Column(db.Integer, nullable=False)
    input_settings = db.Column(db.Blob, nullable=True)
    output_filename = db.Column(db.Blob, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    has_error = db.Column(db.Boolean, nullable=False)
    node_id = db.Column(db.Integer, nullable=True)
    model_id = db.Column(db.Integer, db.ForeignKey('modelrun.run_id'), nullable=False)

    def __init__(self, user_id, run_id, hl_name, sim_name, hl_ver, sim_ver):
        self.user_id = user_id
        self.model_id = run_id
        self.high_level_script_name = hl_name
        self.simulation_name = sim_name
        self.high_level_script_version = hl_ver
        self.simulation_version = sim_ver





class ModelRun(db.Model):
    """


    """
    model_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submission_time = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    completion_time = db.Column(db.DateTime, nullable=True)
    has_error = db.Column(db.Boolean)

    _states = ('Submitted',
               'Running',
               'Completed',
               'Error')

    def __init__(self, user_id):
        self.user_id = user_id
        self.submission_time = datetime.now()

    def __repr__(self):
        return "<Model Run # '%s'>" % self.run_id

    def __str__(self):
        return self.run_id

    def set_complete(self):
        self.completion_time = datetime.now()

    def get_state(self):
        if self.has_error:
            return self._states[3]

        if not self.start_time and not self.completion_time:
            return self._states[0]
        elif self.start_time and not self.completion_time:
            return self._states[1]
        elif self.start_time and self.completion_time:
            return self._states[2]


class Entries(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    device_id = db.Column(db.Text(),  nullable=False)
    device_num = db.Column(db.Integer, db.ForeignKey('devices.id'),nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Device: '%s'>" % self.name

    def __str__(self):
        return self.name

    def __init__(self, user_id, device_num):
        self.user_id = user_id
        self.device_num = device_num
        self.time_stamp = datetime.now()

    def new_entry(self, entry, time_gap=1800):
        if not isinstance(entry, Entries):
            return False

        states_to_compare = ['ambient_temperature_f',
                             'hvac_state',
                             'humidity',
                             'target_temperature_f']

        for states in states_to_compare:
            if getattr(self, states) != getattr(entry, states):
                return True

        # Only update if it has been long enough since last update
        if (self.time_stamp - entry.time_stamp) > timedelta(seconds=time_gap):
            return True

        return False


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    device_id = db.Column(db.Text(), nullable=False)
    name = db.Column(db.Text(), nullable=False)

    user = db.relationship('User',foreign_keys=[user_id])

    def __repr__(self):
        return "<Device: '%s', Id: '%s'>" % (self.name, self.device_id)

    def __str__(self):
        return self.name

    def __init__(self, device_id, user_id, name):
        self.device_id = device_id
        self.user_id = user_id
        self.name = name



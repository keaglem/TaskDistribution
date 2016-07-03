import datetime
import os

import itsdangerous
from flask import current_app
from flask.ext.login import UserMixin
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from .extensions import Base
import sqlalchemy as db


class User(Base, UserMixin):
    __tablename__ = 'user'
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


class Simulation(Base):
    """
    Database for an individual run of the simulation
    """
    __tablename__ = 'simulation'
    simulation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    random_seeding = db.Column(db.Integer, nullable=False)
    input_settings_filename = db.Column(db.Text(), nullable=True)
    output_filename = db.Column(db.Text(), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    has_error = db.Column(db.Boolean, nullable=False)
    node_id = db.Column(db.Integer, nullable=True)
    model_id = db.Column(db.Integer, db.ForeignKey('submission.sub_id'), nullable=False)

    def __init__(self, user_id, run_id):
        self.user_id = user_id
        self.model_id = run_id


class Submission(Base):
    """
    Database for a submission of a set of simulation runs
    """
    __tablename__ = 'submission'
    sub_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submission_time = db.Column(db.DateTime, nullable=False)
    high_level_script_name = db.Column(db.Text(), nullable=False)
    simulation_name = db.Column(db.Text(), nullable=False)
    high_level_script_version = db.Column(db.Integer, nullable=False)
    simulation_version = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    completion_time = db.Column(db.DateTime, nullable=True)
    has_error = db.Column(db.Boolean)
    user = db.orm.relationship('User',foreign_keys=[user_id])

    _states = ('Submitted',
               'Running',
               'Completed',
               'Error')

    def __init__(self, user_id, hl_name, sim_name, hl_ver, sim_ver):
        self.user_id = user_id
        self.submission_time = datetime.now()
        self.high_level_script_name = hl_name
        self.simulation_name = sim_name
        self.high_level_script_version = hl_ver
        self.simulation_version = sim_ver

    def __repr__(self):
        return "<Model Run # '%s'>" % self.sub_id

    def __str__(self):
        return self.sub_id

    def set_complete(self):
        self.completion_time = datetime.now()

    def get_name(self):
        return self.__repr__()


    def get_state(self):
        if self.has_error:
            return self._states[3]

        if not self.start_time and not self.completion_time:
            return self._states[0]
        elif self.start_time and not self.completion_time:
            return self._states[1]
        elif self.start_time and self.completion_time:
            return self._states[2]


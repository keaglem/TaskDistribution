"""Helper functions and decorators."""
import functools

from flask import redirect, url_for, flash
from flask.ext.login import current_user


def admin_required(f):
    """A decorator that will redirect if current user is not an admin."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if getattr(current_user, 'is_admin', False):
            return f(*args, **kwargs)
        flash('You are not authorized to view that page.', 'danger')
        return redirect(url_for('user.submissions'))
    return wrapper


def redirect_logged_in(view, **url_for_kwargs):
    """A decorator that will redirect to the given view if current user is logged on."""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated():
                return redirect(url_for(view, **url_for_kwargs))
            return f(*args, **kwargs)
        return wrapper
    return decorator

def push_notification(text):
    """Send a push notification over a socket.

    The PUSH_NOTIFICATION_PORT setting must be configured. 
    Exceptions will be silenced.
    """

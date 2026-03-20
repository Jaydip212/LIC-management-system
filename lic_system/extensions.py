from flask_mysqldb import MySQL
from flask import session, flash, redirect, url_for
from functools import wraps

mysql = MySQL()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access the admin panel.', 'warning')
            try:
                return redirect(url_for('auth.login'))
            except Exception:
                pass
        return f(*args, **kwargs)
    return decorated

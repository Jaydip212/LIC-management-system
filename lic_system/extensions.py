import pymysql
import pymysql.cursors
from flask import g, current_app, session, flash, redirect, url_for
from functools import wraps

class MySQL:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('MYSQL_HOST', 'localhost')
        app.config.setdefault('MYSQL_USER', None)
        app.config.setdefault('MYSQL_PASSWORD', None)
        app.config.setdefault('MYSQL_DB', None)
        app.config.setdefault('MYSQL_PORT', 3306)
        app.config.setdefault('MYSQL_CURSORCLASS', None)

        @app.teardown_appcontext
        def teardown(exception):
            db = getattr(g, '_mysql_db', None)
            if db is not None:
                db.close()

    @property
    def connection(self):
        ctx = g
        if ctx is not None:
            if not hasattr(ctx, '_mysql_db'):
                cursorclass = pymysql.cursors.DictCursor if current_app.config.get('MYSQL_CURSORCLASS') == 'DictCursor' else pymysql.cursors.Cursor
                ctx._mysql_db = pymysql.connect(
                    host=current_app.config['MYSQL_HOST'],
                    user=current_app.config['MYSQL_USER'],
                    password=current_app.config['MYSQL_PASSWORD'],
                    db=current_app.config['MYSQL_DB'],
                    port=current_app.config['MYSQL_PORT'],
                    cursorclass=cursorclass
                )
            return ctx._mysql_db

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

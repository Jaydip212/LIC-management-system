"""
LIC Management System - Main Flask Application
"""
import os
import math
import pymysql
pymysql.install_as_MySQLdb()          # use PyMySQL as the MySQL driver
from datetime import datetime, date
from flask import Flask, render_template, redirect, url_for, request, \
    session, flash, jsonify
from flask_mysqldb import MySQL
import bcrypt
from config import config


# ─── App Init ───────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(config['default'])

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from extensions import mysql, login_required
mysql.init_app(app)

# ─── Helpers ────────────────────────────────────────────────────────────────
def get_db():
    import MySQLdb
    from extensions import mysql
    cur = mysql.connection.cursor()
    return cur

def paginate(query, args, page, per_page=15):
    """Run a COUNT and a paginated SELECT for a query."""
    cur = get_db()
    cur.execute(f"SELECT COUNT(*) as total FROM ({query}) t", args)
    total = cur.fetchone()['total']
    offset = (page - 1) * per_page
    cur.execute(f"{query} LIMIT %s OFFSET %s", (*args, per_page, offset))
    rows = cur.fetchall()
    cur.close()
    pages = math.ceil(total / per_page) if total else 1
    return rows, total, pages

# ─── Context Processors ─────────────────────────────────────────────────────
@app.context_processor
def inject_globals():
    unread = 0
    if 'admin_id' in session:
        try:
            cur = get_db()
            cur.execute("SELECT COUNT(*) as c FROM contact_messages WHERE is_read=0")
            unread = cur.fetchone()['c']
            cur.close()
        except Exception:
            pass
    return dict(unread_messages=unread, current_year=datetime.now().year)

# Expose Python builtins to Jinja2 templates
app.jinja_env.globals.update(enumerate=enumerate, zip=zip, len=len, int=int)

# ─── Register Blueprints ────────────────────────────────────────────────────
from routes.auth       import auth_bp
from routes.dashboard  import dashboard_bp
from routes.customers  import customers_bp
from routes.policies   import policies_bp
from routes.payments   import payments_bp
from routes.agents     import agents_bp
from routes.claims     import claims_bp
from routes.messages   import messages_bp
from routes.reports    import reports_bp
from routes.public     import public_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(policies_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(agents_bp)
app.register_blueprint(claims_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(public_bp)

# ─── Error Handlers ─────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template('public/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('public/500.html'), 500

# ─── Run ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)

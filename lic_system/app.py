"""
LIC Management System - Main Flask Application
"""
import os
import math
from datetime import datetime, date
from flask import Flask, render_template, redirect, url_for, request, \
    session, flash, jsonify
import bcrypt
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
from config import config


# ─── App Init ───────────────────────────────────────────────────────────────
# Explicitly set paths for Vercel
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir   = os.path.join(os.path.dirname(__file__), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# DIAGNOSTIC: Print directory structure and template folder exists
print(f" * ABS PATH OF __FILE__: {os.path.abspath(__file__)}")
print(f" * TEMPLATE DIR PATH: {template_dir}")
print(f" * TEMPLATE DIR EXISTS: {os.path.exists(template_dir)}")
if os.path.exists(template_dir):
    print(f" * TEMPLATE DIR CONTENTS: {os.listdir(template_dir)}")
else:
    print(f" * ROOT DIR CONTENTS: {os.listdir(os.path.dirname(os.path.abspath(__file__)))}")


# Choose config based on environment
if os.environ.get('VERCEL') or os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object(config['production'])
else:
    app.config.from_object(config['default'])

# Handle SSL CA certificate from environment variable if on Vercel
ca_content = os.environ.get('MYSQL_CA_CERT_CONTENT')
if ca_content and os.environ.get('VERCEL'):
    try:
        ca_path = os.path.join('/tmp', 'ca.pem')
        with open(ca_path, 'w') as f:
            f.write(ca_content)
        app.config['MYSQL_CA_PATH'] = ca_path
    except Exception as e:
        print(f"Error writing CA cert: {e}")

# Ensure upload folder exists
try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
except OSError:
    pass # On read-only environments like Vercel, this will fail but shouldn't crash the app

from extensions import mysql, login_required
print(f" * Using MYSQL_USER: {app.config.get('MYSQL_USER')}")
print(f" * Using MYSQL_HOST: {app.config.get('MYSQL_HOST')}")
mysql.init_app(app)

# ─── Helpers ────────────────────────────────────────────────────────────────
def get_db():
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

@app.route('/debug-paths')
def debug_paths():
    import os
    res = {
        'cwd': os.getcwd(),
        'file': __file__,
        'template_dir': app.template_folder,
        'static_dir': app.static_folder,
        'dir_contents': os.listdir(os.path.dirname(os.path.abspath(__file__))),
        'templates_exists': os.path.exists(app.template_folder)
    }
    if res['templates_exists']:
        res['templates_internal'] = os.listdir(app.template_folder)
    return jsonify(res)

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
    try:
        return render_template('public/404.html'), 404
    except Exception:
        return "404 Not Found", 404

@app.errorhandler(500)
def server_error(e):
    # Log the original error
    import traceback
    error_info = traceback.format_exc()
    print(error_info)
    
    # Diagnostic info
    diag = f"""
    --- DEBUG INFO ---
    ABS PATH OF __FILE__: {os.path.abspath(__file__)}
    CWD: {os.getcwd()}
    TEMPLATE_DIR: {app.template_folder}
    TEMPLATE_DIR EXISTS: {os.path.exists(app.template_folder) if app.template_folder else 'None'}
    """
    try:
        if app.template_folder and os.path.exists(app.template_folder):
            diag += f"\nCONTENTS OF TEMPLATE_DIR: {os.listdir(app.template_folder)}"
        diag += f"\nROOT DIR CONTENTS: {os.listdir(os.path.dirname(os.path.abspath(__file__)))}"
    except Exception as e:
        diag += f"\nDIAG ERROR: {e}"

    try:
        return render_template('public/500.html'), 500
    except Exception as template_err:
        return f"500 Internal Server Error<br><br>Original Error:<pre>{error_info}</pre><br>Template Error: {template_err}<br><br><pre>{diag}</pre>", 500

# ─── Run ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)

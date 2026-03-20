"""
Authentication routes – login / logout
"""
from flask import Blueprint, render_template, redirect, url_for, \
    request, session, flash
from flask_mysqldb import MySQL
import bcrypt
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# We import mysql from app inside functions to avoid circular imports
def get_mysql():
    from extensions import mysql
    return mysql

# ─── Login ──────────────────────────────────────────────────────────────────
@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if 'admin_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter username and password.', 'danger')
            return render_template('admin/login.html')

        mysql = get_mysql()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admins WHERE username=%s OR email=%s",
                    (username, username))
        admin = cur.fetchone()
        cur.close()

        if admin and bcrypt.checkpw(password.encode(), admin['password'].encode()):
            session['admin_id']   = admin['id']
            session['admin_name'] = admin['full_name']
            session['admin_role'] = admin['role']
            # Update last login
            cur = mysql.connection.cursor()
            cur.execute("UPDATE admins SET last_login=%s WHERE id=%s",
                        (datetime.now(), admin['id']))
            mysql.connection.commit()
            cur.close()
            flash(f"Welcome back, {admin['full_name']}!", 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('admin/login.html')

# ─── Logout ─────────────────────────────────────────────────────────────────
@auth_bp.route('/admin/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

"""
Policy management routes
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from extensions import mysql, login_required

policies_bp = Blueprint('policies', __name__)

@policies_bp.route('/admin/policies')
@login_required
def index():
    q    = request.args.get('q', '')
    ptype = request.args.get('type', '')
    page = int(request.args.get('page', 1)); per = 15
    where = "WHERE 1=1"; params = []
    if q:
        where += " AND (policy_name LIKE %s OR policy_code LIKE %s)"
        params.extend([f'%{q}%', f'%{q}%'])
    if ptype:
        where += " AND policy_type=%s"; params.append(ptype)
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT COUNT(*) as c FROM policies {where}", params)
    total = cur.fetchone()['c']; pages = max(1, -(-total // per))
    cur.execute(f"SELECT * FROM policies {where} ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (*params, per, (page-1)*per))
    policies = cur.fetchall(); cur.close()
    return render_template('admin/policies.html', policies=policies, q=q,
                           ptype=ptype, page=page, pages=pages, total=total)

@policies_bp.route('/admin/policies/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        f = request.form
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) as c FROM policies"); n = cur.fetchone()['c'] + 1
        code = f"POL{n:04d}"
        try:
            cur.execute("""INSERT INTO policies
                (policy_code,policy_name,policy_type,coverage_amount,premium_amount,
                 duration_years,benefits,description,status)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (code, f['policy_name'], f['policy_type'], f['coverage_amount'],
                 f['premium_amount'], f['duration_years'], f.get('benefits'),
                 f.get('description'), f.get('status','active')))
            mysql.connection.commit(); cur.close()
            flash(f'Policy added successfully! (Code: {code})', 'success')
            return redirect(url_for('policies.index'))
        except Exception as e:
            mysql.connection.rollback(); cur.close()
            flash(f'Error: {str(e)}', 'danger')
    return render_template('admin/policy_form.html', policy=None)

@policies_bp.route('/admin/policies/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def edit(pid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM policies WHERE id=%s", (pid,))
    policy = cur.fetchone(); cur.close()
    if not policy:
        flash('Policy not found.', 'danger'); return redirect(url_for('policies.index'))
    if request.method == 'POST':
        f = request.form
        cur = mysql.connection.cursor()
        try:
            cur.execute("""UPDATE policies SET policy_name=%s, policy_type=%s,
                coverage_amount=%s, premium_amount=%s, duration_years=%s,
                benefits=%s, description=%s, status=%s WHERE id=%s""",
                (f['policy_name'], f['policy_type'], f['coverage_amount'],
                 f['premium_amount'], f['duration_years'], f.get('benefits'),
                 f.get('description'), f.get('status','active'), pid))
            mysql.connection.commit(); cur.close()
            flash('Policy updated successfully!', 'success')
            return redirect(url_for('policies.index'))
        except Exception as e:
            mysql.connection.rollback(); cur.close()
            flash(f'Error: {str(e)}', 'danger')
    return render_template('admin/policy_form.html', policy=policy)

@policies_bp.route('/admin/policies/delete/<int:pid>', methods=['POST'])
@login_required
def delete(pid):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM policies WHERE id=%s", (pid,))
        mysql.connection.commit(); flash('Policy deleted.', 'success')
    except Exception as e:
        mysql.connection.rollback(); flash(f'Cannot delete: {str(e)}', 'danger')
    finally: cur.close()
    return redirect(url_for('policies.index'))

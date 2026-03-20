"""
Claim management routes
"""
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from extensions import mysql, login_required
from werkzeug.utils import secure_filename
from config import Config

claims_bp = Blueprint('claims', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in Config.ALLOWED_EXTENSIONS

@claims_bp.route('/admin/claims')
@login_required
def index():
    q = request.args.get('q',''); status = request.args.get('status','')
    page = int(request.args.get('page',1)); per = 15
    where = "WHERE 1=1"; params = []
    if q:
        where += " AND (c.full_name LIKE %s OR cl.claim_code LIKE %s)"
        params.extend([f'%{q}%']*2)
    if status:
        where += " AND cl.status=%s"; params.append(status)
    cur = mysql.connection.cursor()
    cur.execute(f"""SELECT COUNT(*) as c FROM claims cl
        JOIN customers c ON cl.customer_id=c.id {where}""", params)
    total = cur.fetchone()['c']; pages = max(1,-(-total//per))
    cur.execute(f"""
        SELECT cl.*, c.full_name, c.customer_code, pol.policy_name
        FROM claims cl JOIN customers c ON cl.customer_id=c.id
        JOIN policies pol ON cl.policy_id=pol.id
        {where} ORDER BY cl.created_at DESC LIMIT %s OFFSET %s
    """, (*params, per, (page-1)*per))
    claims = cur.fetchall(); cur.close()
    return render_template('admin/claims.html', claims=claims, q=q,
        status=status, page=page, pages=pages, total=total)

@claims_bp.route('/admin/claims/add', methods=['GET','POST'])
@login_required
def add():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id,full_name,customer_code FROM customers WHERE status='active'")
    customers = cur.fetchall()
    cur.execute("SELECT id,policy_name FROM policies WHERE status='active'")
    policies = cur.fetchall(); cur.close()
    if request.method == 'POST':
        f = request.form; cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) as c FROM claims"); n = cur.fetchone()['c']+1
        code = f"CLM{n:04d}"
        doc_path = None
        if 'document' in request.files:
            file = request.files['document']
            if file and file.filename and allowed_file(file.filename):
                fn = secure_filename(file.filename)
                fp = os.path.join(Config.UPLOAD_FOLDER, fn)
                file.save(fp); doc_path = fn
        try:
            cur.execute("""INSERT INTO claims
                (claim_code,customer_id,policy_id,claim_type,claim_amount,claim_date,
                 incident_date,incident_description,document_path,status,remarks)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (code,f['customer_id'],f['policy_id'],f['claim_type'],f['claim_amount'],
                 f['claim_date'],f.get('incident_date') or None,
                 f.get('incident_description'),doc_path,
                 f.get('status','pending'),f.get('remarks')))
            mysql.connection.commit(); cur.close()
            flash(f'Claim added! (Code: {code})', 'success')
            return redirect(url_for('claims.index'))
        except Exception as e:
            mysql.connection.rollback(); cur.close()
            flash(f'Error: {str(e)}', 'danger')
    return render_template('admin/claim_form.html', claim=None,
                           customers=customers, policies=policies)

@claims_bp.route('/admin/claims/edit/<int:cid>', methods=['GET','POST'])
@login_required
def edit(cid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM claims WHERE id=%s", (cid,))
    claim = cur.fetchone()
    cur.execute("SELECT id,full_name,customer_code FROM customers WHERE status='active'")
    customers = cur.fetchall()
    cur.execute("SELECT id,policy_name FROM policies WHERE status='active'")
    policies = cur.fetchall(); cur.close()
    if not claim:
        flash('Claim not found.', 'danger'); return redirect(url_for('claims.index'))
    if request.method == 'POST':
        f = request.form; cur = mysql.connection.cursor()
        try:
            cur.execute("""UPDATE claims SET customer_id=%s,policy_id=%s,claim_type=%s,
                claim_amount=%s,claim_date=%s,incident_date=%s,incident_description=%s,
                status=%s,remarks=%s,resolved_date=%s WHERE id=%s""",
                (f['customer_id'],f['policy_id'],f['claim_type'],f['claim_amount'],
                 f['claim_date'],f.get('incident_date') or None,
                 f.get('incident_description'),f.get('status','pending'),
                 f.get('remarks'),f.get('resolved_date') or None,cid))
            mysql.connection.commit(); cur.close()
            flash('Claim updated!', 'success')
            return redirect(url_for('claims.index'))
        except Exception as e:
            mysql.connection.rollback(); cur.close()
            flash(f'Error: {str(e)}', 'danger')
    return render_template('admin/claim_form.html', claim=claim,
                           customers=customers, policies=policies)

@claims_bp.route('/admin/claims/delete/<int:cid>', methods=['POST'])
@login_required
def delete(cid):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM claims WHERE id=%s",(cid,))
        mysql.connection.commit(); flash('Claim deleted.', 'success')
    except Exception as e:
        mysql.connection.rollback(); flash(f'Error: {str(e)}', 'danger')
    finally: cur.close()
    return redirect(url_for('claims.index'))

"""
Premium payment management routes
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from extensions import mysql, login_required
from datetime import datetime

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/admin/payments')
@login_required
def index():
    q      = request.args.get('q', '')
    status = request.args.get('status', '')
    page   = int(request.args.get('page', 1)); per = 15
    where  = "WHERE 1=1"; params = []
    if q:
        where += " AND (c.full_name LIKE %s OR pp.payment_code LIKE %s OR pp.receipt_number LIKE %s)"
        params.extend([f'%{q}%']*3)
    if status:
        where += " AND pp.status=%s"; params.append(status)
    cur = mysql.connection.cursor()
    cur.execute(f"""SELECT COUNT(*) as c FROM premium_payments pp
        JOIN customers c ON pp.customer_id=c.id {where}""", params)
    total = cur.fetchone()['c']; pages = max(1, -(-total // per))
    cur.execute(f"""
        SELECT pp.*, c.full_name, c.customer_code, pol.policy_name
        FROM premium_payments pp
        JOIN customers c ON pp.customer_id=c.id
        JOIN policies pol ON pp.policy_id=pol.id
        {where} ORDER BY pp.created_at DESC LIMIT %s OFFSET %s
    """, (*params, per, (page-1)*per))
    payments = cur.fetchall()
    # Summary cards
    cur.execute("SELECT SUM(amount) as s FROM premium_payments WHERE status='paid'")
    paid_total = cur.fetchone()['s'] or 0
    cur.execute("SELECT COUNT(*) as c FROM premium_payments WHERE status='overdue'")
    overdue_count = cur.fetchone()['c']
    cur.close()
    return render_template('admin/payments.html', payments=payments, q=q,
        status=status, page=page, pages=pages, total=total,
        paid_total=paid_total, overdue_count=overdue_count)

@payments_bp.route('/admin/payments/add', methods=['GET', 'POST'])
@login_required
def add():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, full_name, customer_code, policy_id FROM customers WHERE status='active'")
    customers = cur.fetchall()
    cur.execute("SELECT id, policy_name, premium_amount FROM policies WHERE status='active'")
    policies = cur.fetchall()
    cur.close()
    if request.method == 'POST':
        f = request.form
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) as c FROM premium_payments"); n = cur.fetchone()['c']+1
        code = f"PAY{n:04d}"
        try:
            cur.execute("""INSERT INTO premium_payments
                (payment_code,customer_id,policy_id,amount,due_date,payment_date,
                 payment_mode,status,receipt_number,remarks)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (code, f['customer_id'], f['policy_id'], f['amount'],
                 f['due_date'], f.get('payment_date') or None,
                 f.get('payment_mode','online'), f.get('status','pending'),
                 f.get('receipt_number') or None, f.get('remarks')))
            mysql.connection.commit(); cur.close()
            flash(f'Payment record added! (Code: {code})', 'success')
            return redirect(url_for('payments.index'))
        except Exception as e:
            mysql.connection.rollback(); cur.close()
            flash(f'Error: {str(e)}', 'danger')
    return render_template('admin/payment_form.html', payment=None,
                           customers=customers, policies=policies)

@payments_bp.route('/admin/payments/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def edit(pid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM premium_payments WHERE id=%s", (pid,))
    payment = cur.fetchone()
    cur.execute("SELECT id, full_name, customer_code FROM customers WHERE status='active'")
    customers = cur.fetchall()
    cur.execute("SELECT id, policy_name, premium_amount FROM policies WHERE status='active'")
    policies = cur.fetchall()
    cur.close()
    if not payment:
        flash('Payment not found.', 'danger'); return redirect(url_for('payments.index'))
    if request.method == 'POST':
        f = request.form; cur = mysql.connection.cursor()
        try:
            cur.execute("""UPDATE premium_payments SET
                customer_id=%s, policy_id=%s, amount=%s, due_date=%s,
                payment_date=%s, payment_mode=%s, status=%s,
                receipt_number=%s, remarks=%s WHERE id=%s""",
                (f['customer_id'], f['policy_id'], f['amount'], f['due_date'],
                 f.get('payment_date') or None, f.get('payment_mode','online'),
                 f.get('status','pending'), f.get('receipt_number') or None,
                 f.get('remarks'), pid))
            mysql.connection.commit(); cur.close()
            flash('Payment updated!', 'success')
            return redirect(url_for('payments.index'))
        except Exception as e:
            mysql.connection.rollback(); cur.close()
            flash(f'Error: {str(e)}', 'danger')
    return render_template('admin/payment_form.html', payment=payment,
                           customers=customers, policies=policies)

@payments_bp.route('/admin/payments/delete/<int:pid>', methods=['POST'])
@login_required
def delete(pid):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM premium_payments WHERE id=%s", (pid,))
        mysql.connection.commit(); flash('Payment deleted.', 'success')
    except Exception as e:
        mysql.connection.rollback(); flash(f'Error: {str(e)}', 'danger')
    finally: cur.close()
    return redirect(url_for('payments.index'))

"""
Customer management routes – CRUD + search
"""
from flask import Blueprint, render_template, redirect, url_for, \
    request, flash, jsonify
from extensions import mysql, login_required

customers_bp = Blueprint('customers', __name__)

# ─── List ────────────────────────────────────────────────────────────────────
@customers_bp.route('/admin/customers')
@login_required
def index():
    q      = request.args.get('q', '')
    status = request.args.get('status', '')
    page   = int(request.args.get('page', 1))
    per    = 15

    where  = "WHERE 1=1"
    params = []
    if q:
        where += " AND (c.full_name LIKE %s OR c.mobile LIKE %s OR c.customer_code LIKE %s OR c.email LIKE %s)"
        params.extend([f'%{q}%'] * 4)
    if status:
        where += " AND c.status = %s"
        params.append(status)

    cur = mysql.connection.cursor()
    cur.execute(f"SELECT COUNT(*) as cnt FROM customers c {where}", params)
    total = cur.fetchone()['cnt']
    pages = max(1, -(-total // per))
    offset = (page - 1) * per

    cur.execute(f"""
        SELECT c.*, p.policy_name, p.policy_type, a.full_name as agent_name
        FROM customers c
        LEFT JOIN policies p ON c.policy_id = p.id
        LEFT JOIN agents a ON c.agent_id = a.id
        {where}
        ORDER BY c.created_at DESC LIMIT %s OFFSET %s
    """, (*params, per, offset))
    customers = cur.fetchall()
    cur.close()

    return render_template('admin/customers.html',
        customers=customers, q=q, status=status,
        page=page, pages=pages, total=total)


# ─── Add ─────────────────────────────────────────────────────────────────────
@customers_bp.route('/admin/customers/add', methods=['GET', 'POST'])
@login_required
def add():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id,policy_name,policy_type FROM policies WHERE status='active'")
    policies = cur.fetchall()
    cur.execute("SELECT id,full_name,agent_code FROM agents WHERE status='active'")
    agents = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        f = request.form
        # Auto-generate customer code
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) as c FROM customers")
        n = cur.fetchone()['c'] + 1
        code = f"CUS{n:04d}"
        try:
            cur.execute("""
                INSERT INTO customers
                (customer_code, full_name, email, mobile, address, city, state, pincode,
                 date_of_birth, gender, nominee_name, nominee_relation,
                 policy_id, agent_id, policy_start_date, policy_end_date, sum_assured, status)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                code,
                f.get('full_name'), f.get('email'), f.get('mobile'),
                f.get('address'), f.get('city'), f.get('state'), f.get('pincode'),
                f.get('date_of_birth') or None, f.get('gender'),
                f.get('nominee_name'), f.get('nominee_relation'),
                f.get('policy_id') or None, f.get('agent_id') or None,
                f.get('policy_start_date') or None, f.get('policy_end_date') or None,
                f.get('sum_assured') or None, f.get('status', 'active')
            ))
            mysql.connection.commit()
            cur.close()
            flash(f'Customer {f.get("full_name")} added successfully! (Code: {code})', 'success')
            return redirect(url_for('customers.index'))
        except Exception as e:
            mysql.connection.rollback()
            cur.close()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('admin/customer_form.html',
        customer=None, policies=policies, agents=agents)


# ─── Edit ────────────────────────────────────────────────────────────────────
@customers_bp.route('/admin/customers/edit/<int:cid>', methods=['GET', 'POST'])
@login_required
def edit(cid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers WHERE id=%s", (cid,))
    customer = cur.fetchone()
    if not customer:
        flash('Customer not found.', 'danger')
        return redirect(url_for('customers.index'))

    cur.execute("SELECT id,policy_name,policy_type FROM policies WHERE status='active'")
    policies = cur.fetchall()
    cur.execute("SELECT id,full_name,agent_code FROM agents WHERE status='active'")
    agents = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        f = request.form
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                UPDATE customers SET
                  full_name=%s, email=%s, mobile=%s, address=%s, city=%s, state=%s, pincode=%s,
                  date_of_birth=%s, gender=%s, nominee_name=%s, nominee_relation=%s,
                  policy_id=%s, agent_id=%s, policy_start_date=%s, policy_end_date=%s,
                  sum_assured=%s, status=%s
                WHERE id=%s
            """, (
                f.get('full_name'), f.get('email'), f.get('mobile'),
                f.get('address'), f.get('city'), f.get('state'), f.get('pincode'),
                f.get('date_of_birth') or None, f.get('gender'),
                f.get('nominee_name'), f.get('nominee_relation'),
                f.get('policy_id') or None, f.get('agent_id') or None,
                f.get('policy_start_date') or None, f.get('policy_end_date') or None,
                f.get('sum_assured') or None, f.get('status', 'active'),
                cid
            ))
            mysql.connection.commit()
            cur.close()
            flash('Customer updated successfully!', 'success')
            return redirect(url_for('customers.index'))
        except Exception as e:
            mysql.connection.rollback()
            cur.close()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('admin/customer_form.html',
        customer=customer, policies=policies, agents=agents)


# ─── Delete ──────────────────────────────────────────────────────────────────
@customers_bp.route('/admin/customers/delete/<int:cid>', methods=['POST'])
@login_required
def delete(cid):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM customers WHERE id=%s", (cid,))
        mysql.connection.commit()
        flash('Customer deleted successfully.', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Cannot delete: {str(e)}', 'danger')
    finally:
        cur.close()
    return redirect(url_for('customers.index'))


# ─── View ────────────────────────────────────────────────────────────────────
@customers_bp.route('/admin/customers/view/<int:cid>')
@login_required
def view(cid):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.*, p.policy_name, p.policy_type, p.coverage_amount,
               a.full_name as agent_name, a.agent_code, a.mobile as agent_mobile
        FROM customers c
        LEFT JOIN policies p ON c.policy_id = p.id
        LEFT JOIN agents a ON c.agent_id = a.id
        WHERE c.id=%s
    """, (cid,))
    customer = cur.fetchone()
    if not customer:
        flash('Customer not found.', 'danger')
        return redirect(url_for('customers.index'))

    cur.execute("""
        SELECT pp.*, pol.policy_name FROM premium_payments pp
        JOIN policies pol ON pp.policy_id = pol.id
        WHERE pp.customer_id=%s ORDER BY pp.due_date DESC
    """, (cid,))
    payments = cur.fetchall()

    cur.execute("""
        SELECT cl.*, pol.policy_name FROM claims cl
        JOIN policies pol ON cl.policy_id = pol.id
        WHERE cl.customer_id=%s ORDER BY cl.claim_date DESC
    """, (cid,))
    claims = cur.fetchall()
    cur.close()

    return render_template('admin/customer_view.html',
        customer=customer, payments=payments, claims=claims)

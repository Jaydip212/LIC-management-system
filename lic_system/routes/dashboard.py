"""
Dashboard routes – overview analytics
"""
from flask import Blueprint, render_template, session, redirect, url_for
from extensions import mysql, login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/admin')
@dashboard_bp.route('/admin/dashboard')
@login_required
def index():
    cur = mysql.connection.cursor()

    # KPI counts
    cur.execute("SELECT COUNT(*) as c FROM customers WHERE status='active'")
    total_customers = cur.fetchone()['c']

    cur.execute("SELECT COUNT(*) as c FROM policies WHERE status='active'")
    total_policies = cur.fetchone()['c']

    cur.execute("SELECT COUNT(*) as c FROM agents WHERE status='active'")
    total_agents = cur.fetchone()['c']

    cur.execute("SELECT COALESCE(SUM(amount),0) as s FROM premium_payments WHERE status='paid'")
    total_collected = cur.fetchone()['s']

    cur.execute("SELECT COUNT(*) as c FROM premium_payments WHERE status='pending'")
    pending_payments = cur.fetchone()['c']

    cur.execute("SELECT COUNT(*) as c FROM premium_payments WHERE status='overdue'")
    overdue_payments = cur.fetchone()['c']

    cur.execute("SELECT COUNT(*) as c FROM claims WHERE status='pending'")
    pending_claims = cur.fetchone()['c']

    cur.execute("SELECT COUNT(*) as c FROM contact_messages WHERE is_read=0")
    unread_msgs = cur.fetchone()['c']

    # Recent customers
    cur.execute("""
        SELECT c.customer_code, c.full_name, c.mobile, c.status,
               p.policy_name, c.created_at
        FROM customers c
        LEFT JOIN policies p ON c.policy_id = p.id
        ORDER BY c.created_at DESC LIMIT 6
    """)
    recent_customers = cur.fetchall()

    # Recent payments
    cur.execute("""
        SELECT pp.payment_code, c.full_name, pp.amount,
               pp.due_date, pp.status, pp.payment_mode
        FROM premium_payments pp
        JOIN customers c ON pp.customer_id = c.id
        ORDER BY pp.created_at DESC LIMIT 6
    """)
    recent_payments = cur.fetchall()

    # Recent claims
    cur.execute("""
        SELECT cl.claim_code, c.full_name, cl.claim_type,
               cl.claim_amount, cl.status, cl.claim_date
        FROM claims cl
        JOIN customers c ON cl.customer_id = c.id
        ORDER BY cl.created_at DESC LIMIT 5
    """)
    recent_claims = cur.fetchall()

    # Monthly collection (last 6 months)
    cur.execute("""
        SELECT DATE_FORMAT(payment_date,'%b %Y') as month,
               SUM(amount) as total
        FROM premium_payments
        WHERE status='paid' AND payment_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY YEAR(payment_date), MONTH(payment_date), DATE_FORMAT(payment_date,'%b %Y')
        ORDER BY YEAR(payment_date) ASC, MONTH(payment_date) ASC
    """)
    monthly_data = cur.fetchall()
    cur.close()

    return render_template('admin/dashboard.html',
        total_customers=total_customers,
        total_policies=total_policies,
        total_agents=total_agents,
        total_collected=total_collected,
        pending_payments=pending_payments,
        overdue_payments=overdue_payments,
        pending_claims=pending_claims,
        unread_msgs=unread_msgs,
        recent_customers=recent_customers,
        recent_payments=recent_payments,
        recent_claims=recent_claims,
        monthly_data=monthly_data,
    )

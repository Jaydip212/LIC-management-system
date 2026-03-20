"""
Reports / analytics routes
"""
from flask import Blueprint, render_template
from extensions import mysql, login_required

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/admin/reports')
@login_required
def index():
    cur = mysql.connection.cursor()
    # Monthly premiums collected - last 12 months
    cur.execute("""
        SELECT DATE_FORMAT(payment_date,'%b %Y') as month,
               SUM(amount) as total, COUNT(*) as count
        FROM premium_payments WHERE status='paid'
        AND payment_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        GROUP BY YEAR(payment_date), MONTH(payment_date)
        ORDER BY payment_date ASC
    """)
    monthly_premium = cur.fetchall()
    # Policy type distribution
    cur.execute("""
        SELECT p.policy_type, COUNT(c.id) as customer_count
        FROM policies p LEFT JOIN customers c ON p.id=c.policy_id
        GROUP BY p.policy_type
    """)
    policy_dist = cur.fetchall()
    # Top agents by customer count
    cur.execute("""
        SELECT a.full_name, a.agent_code, COUNT(c.id) as customers,
               SUM(pp.amount) as total_premium
        FROM agents a
        LEFT JOIN customers c ON a.id=c.agent_id
        LEFT JOIN premium_payments pp ON c.id=pp.customer_id AND pp.status='paid'
        GROUP BY a.id ORDER BY customers DESC LIMIT 5
    """)
    top_agents = cur.fetchall()
    # Claims summary by status
    cur.execute("""SELECT status, COUNT(*) as cnt, COALESCE(SUM(claim_amount),0) as total
        FROM claims GROUP BY status""")
    claims_summary = cur.fetchall()
    # Payment status distribution
    cur.execute("SELECT status, COUNT(*) as c, COALESCE(SUM(amount),0) as s FROM premium_payments GROUP BY status")
    payment_summary = cur.fetchall()
    cur.close()
    return render_template('admin/reports.html',
        monthly_premium=monthly_premium, policy_dist=policy_dist,
        top_agents=top_agents, claims_summary=claims_summary,
        payment_summary=payment_summary)

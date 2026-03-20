"""
Agent management routes
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from extensions import mysql, login_required

agents_bp = Blueprint('agents', __name__)

@agents_bp.route('/admin/agents')
@login_required
def index():
    q = request.args.get('q', ''); page = int(request.args.get('page', 1)); per = 15
    where = "WHERE 1=1"; params = []
    if q:
        where += " AND (full_name LIKE %s OR agent_code LIKE %s OR mobile LIKE %s)"
        params.extend([f'%{q}%']*3)
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT COUNT(*) as c FROM agents {where}", params)
    total = cur.fetchone()['c']; pages = max(1, -(-total // per))
    cur.execute(f"""SELECT a.*, (SELECT COUNT(*) FROM customers WHERE agent_id=a.id) as customer_count
        FROM agents a {where} ORDER BY a.created_at DESC LIMIT %s OFFSET %s""",
        (*params, per, (page-1)*per))
    agents = cur.fetchall(); cur.close()
    return render_template('admin/agents.html', agents=agents, q=q,
                           page=page, pages=pages, total=total)

@agents_bp.route('/admin/agents/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        f = request.form; cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) as c FROM agents"); n = cur.fetchone()['c']+1
        code = f"AGT{n:04d}"
        try:
            cur.execute("""INSERT INTO agents
                (agent_code,full_name,email,mobile,address,city,state,
                 license_number,commission_rate,status,joined_date)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (code, f['full_name'], f['email'], f['mobile'],
                 f.get('address'), f.get('city'), f.get('state'),
                 f.get('license_number'), f.get('commission_rate',5),
                 f.get('status','active'), f.get('joined_date') or None))
            mysql.connection.commit(); cur.close()
            flash(f'Agent added! (Code: {code})', 'success')
            return redirect(url_for('agents.index'))
        except Exception as e:
            mysql.connection.rollback(); cur.close()
            flash(f'Error: {str(e)}', 'danger')
    return render_template('admin/agent_form.html', agent=None)

@agents_bp.route('/admin/agents/edit/<int:aid>', methods=['GET', 'POST'])
@login_required
def edit(aid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM agents WHERE id=%s", (aid,))
    agent = cur.fetchone(); cur.close()
    if not agent:
        flash('Agent not found.', 'danger'); return redirect(url_for('agents.index'))
    if request.method == 'POST':
        f = request.form; cur = mysql.connection.cursor()
        try:
            cur.execute("""UPDATE agents SET full_name=%s,email=%s,mobile=%s,address=%s,
                city=%s,state=%s,license_number=%s,commission_rate=%s,status=%s,joined_date=%s
                WHERE id=%s""",
                (f['full_name'], f['email'], f['mobile'], f.get('address'),
                 f.get('city'), f.get('state'), f.get('license_number'),
                 f.get('commission_rate',5), f.get('status','active'),
                 f.get('joined_date') or None, aid))
            mysql.connection.commit(); cur.close()
            flash('Agent updated!', 'success')
            return redirect(url_for('agents.index'))
        except Exception as e:
            mysql.connection.rollback(); cur.close()
            flash(f'Error: {str(e)}', 'danger')
    return render_template('admin/agent_form.html', agent=agent)

@agents_bp.route('/admin/agents/delete/<int:aid>', methods=['POST'])
@login_required
def delete(aid):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM agents WHERE id=%s", (aid,))
        mysql.connection.commit(); flash('Agent deleted.', 'success')
    except Exception as e:
        mysql.connection.rollback(); flash(f'Error: {str(e)}', 'danger')
    finally: cur.close()
    return redirect(url_for('agents.index'))

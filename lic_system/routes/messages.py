"""
Contact messages routes
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from extensions import mysql, login_required

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/admin/messages')
@login_required
def index():
    q = request.args.get('q',''); page = int(request.args.get('page',1)); per = 15
    where = "WHERE 1=1"; params = []
    if q:
        where += " AND (name LIKE %s OR email LIKE %s OR subject LIKE %s)"
        params.extend([f'%{q}%']*3)
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT COUNT(*) as c FROM contact_messages {where}", params)
    total = cur.fetchone()['c']; pages = max(1,-(-total//per))
    cur.execute(f"SELECT * FROM contact_messages {where} ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (*params, per, (page-1)*per))
    msgs = cur.fetchall(); cur.close()
    return render_template('admin/messages.html', msgs=msgs, q=q,
                           page=page, pages=pages, total=total)

@messages_bp.route('/admin/messages/read/<int:mid>')
@login_required
def mark_read(mid):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE contact_messages SET is_read=1 WHERE id=%s",(mid,))
    mysql.connection.commit(); cur.close()
    return redirect(url_for('messages.index'))

@messages_bp.route('/admin/messages/delete/<int:mid>', methods=['POST'])
@login_required
def delete(mid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contact_messages WHERE id=%s",(mid,))
    mysql.connection.commit(); cur.close()
    flash('Message deleted.', 'success')
    return redirect(url_for('messages.index'))

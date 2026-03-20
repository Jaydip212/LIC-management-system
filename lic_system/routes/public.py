"""
Public website routes
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from extensions import mysql

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM policies WHERE status='active' LIMIT 6")
    policies = cur.fetchall()
    cur.close()
    return render_template('main_site/index.html', policies=policies)

@public_bp.route('/about')
def about():
    return render_template('main_site/about.html')

@public_bp.route('/services')
def services():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM policies WHERE status='active' ORDER BY policy_type")
    policies = cur.fetchall()
    cur.close()
    return render_template('main_site/services.html', policies=policies)

@public_bp.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        f = request.form
        name    = f.get('name','').strip()
        phone   = f.get('phone','').strip()
        email   = f.get('email','').strip()
        subject = f.get('subject','').strip()
        message = f.get('message','').strip()
        if not name or not email or not message:
            flash('Please fill all required fields.', 'danger')
        else:
            cur = mysql.connection.cursor()
            try:
                cur.execute("""INSERT INTO contact_messages (name,phone,email,subject,message)
                    VALUES(%s,%s,%s,%s,%s)""",
                    (name,phone,email,subject,message))
                mysql.connection.commit(); cur.close()
                flash('Thank you! Your message has been sent. We\'ll respond within 24 hours.', 'success')
                return redirect(url_for('public.contact'))
            except Exception as e:
                mysql.connection.rollback(); cur.close()
                flash('Error sending message. Please try again.', 'danger')
    return render_template('main_site/contact.html')

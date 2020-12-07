import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from random import randint
from verification_sms import VerificationSMS
import os

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/verify', methods=('GET', 'POST'))
def verify():
    if request.method == 'POST':
        username = request.args['messages']
        vcode = request.form['vcode']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT id, vcode, verified FROM user WHERE username = ?', (username,)
        ).fetchone() 
        print("User code is", user["vcode"])
        print("Request code is ", )
        if user['verified'] is True:
            error = "User is already verified!"
        elif vcode != user['vcode']:
            error = "Incorrect code! Try again!"
        
        if error is None:
            
            db.execute(
                'UPDATE user SET verified = ? WHERE username = ?',
                (1, username)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/verify.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        vcode = ''.join(["{}".format(randint(0, 9)) for num in range(0, 4)])
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not phone:
            error = 'Phone is required'
        elif db.execute(
            'SELECT id FROM user WHERE username = ? OR phone = ?', (username,phone,)
        ).fetchone() is not None:
            error = 'User {} is already registered under this username and/or phone number.'.format(username)
        
        if error is None:
            g_email = os.environ['GMAIL_ADDRESS']
            g_password = os.environ['GMAIL_PASSWORD']
            vms = VerificationSMS()
            if g_email is None or g_password is None:
                abort()
            vms.send_message(g_email, g_password , phone, vcode)
            db.execute(
                'INSERT INTO user (username, password, phone, vcode) VALUES (?, ?, ?, ?)',
                (username, generate_password_hash(password), phone, vcode)
            )
            db.commit()
            return redirect(url_for('auth.verify', messages=username))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        print(user['verified'])
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        elif user['verified'] == False:
            error = 'User is not verified!'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

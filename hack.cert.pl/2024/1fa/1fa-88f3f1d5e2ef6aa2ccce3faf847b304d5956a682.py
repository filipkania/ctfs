import bcrypt

from flask import Flask, render_template, request, url_for, redirect, session, send_from_directory, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user

import pyotp
import qrcode
import qrcode.image.svg


app = Flask(__name__, static_url_path="/", static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(60), nullable=False)
    type = db.Column(db.Integer, nullable=False, default=0)
    mfa_secret = db.Column(db.String(32))


db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    if request.method == 'GET':
        return render_template('register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    password_rep = request.form.get('password_rep')

    if login is None or len(login) < 1:
        return render_template('register.html', message='Missing username!', type='warning')

    if password is None or len(password) < 1:
        return render_template('register.html', message='Missing password!', type='warning')

    if password != password_rep:
        return render_template('register.html', message='Passwords doesn\'t match!', type='warning')

    if len(password) < 8:
        return render_template('register.html', message='Password is too short!', type='warning')

    if User.query.filter_by(login=login).first() is not None:
        return render_template('register.html', message='Username already taken!', type='warning')

    db.session.add(User(
        login=login,
        password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    ))
    db.session.commit()

    return render_template('login.html', message='Registration successful!')


def new_totp(mfa_secret, login):
    return pyotp.totp.TOTP(mfa_secret)


def qr_image(totp, login):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=0,
        image_factory=qrcode.image.svg.SvgPathImage
    )
    qr.add_data(totp.provisioning_uri(
        name=login,
        issuer_name='Kubica fanclub'
    ))

    return qr.make_image().to_string().decode('utf-8')


@app.route('/mfa-setup', methods=['GET', 'POST'])
def mfa_setup():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'new_mfa_secret' not in session.keys():
            return redirect(url_for('mfa_setup'))

        totp = pyotp.totp.TOTP(session['new_mfa_secret'])
        if not totp.verify(request.form.get('mfa_code')):
            qr = qr_image(totp, current_user.login)

            return render_template('mfa-setup.html', qr=qr, message='MFA setup fail!', type='warning')

        current_user.mfa_secret = session['new_mfa_secret']
        db.session.commit()

        session['new_mfa_secret'] = pyotp.random_base32()
        totp = pyotp.totp.TOTP(session['new_mfa_secret'])
        qr = qr_image(totp, current_user.login)

        return render_template('mfa-setup.html', qr=qr, message='MFA setup successful!', type='info')

    session['new_mfa_secret'] = pyotp.random_base32()
    totp = pyotp.totp.TOTP(session['new_mfa_secret'])
    qr = qr_image(totp, current_user.login)

    return render_template('mfa-setup.html', qr=qr)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    if request.method == 'GET':
        return render_template('login.html')

    login = request.form.get('login')
    password = str(request.form.get('password'))

    user = User.query.filter_by(login=login).first()

    user_password = b'$2b$12$0ugUTL6SuPn4diOsot5mTOFgbOutA8WL2NSRBvYJDs2/LXxRypoOW' # based on random uuid, just to ensure equal execution times regardless of whether the user exists or not
    if user is not None:
        user_password = user.password

    result = bcrypt.checkpw(password.encode('utf-8'), user_password)

    if not result:
        return render_template('login.html', message='Wrong username or password!', type='warning')

    if user.mfa_secret is not None:
        session['user'] = user
        session['mfa_login'] = user.login
        return redirect(url_for('mfa'))

    login_user(user)

    return redirect(url_for('root'))


@app.route('/mfa', methods=['GET', 'POST'])
def mfa():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    if request.method == 'GET':
        mfa_login = session.get('mfa_login', None)
        if mfa_login is None:
            return redirect(url_for('login'))

        session['mfa_user'] = User.query.filter_by(login=mfa_login).first()
        if session['mfa_user'] is None:
            return redirect(url_for('login'))

        return render_template('mfa.html')

    mfa_user = session.get('mfa_user', None)
    totp = pyotp.TOTP(mfa_user.mfa_secret)
    if totp.verify(request.form.get('mfa_code')):
        login_user(session.get('user', None))
        return redirect(url_for('root'))

    return render_template('mfa.html', message='MFA verification failed!', type='warning')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'new_mfa_secret' in session.keys():
        session.pop('new_mfa_secret')

    logout_user()

    return redirect(url_for('root'))


@app.route('/', methods=['GET'])
def root():
    if not current_user.is_authenticated:
        return render_template('root-unauth.html')

    return render_template('root.html', flag=current_user.type)

if __name__ == '__main__':
    app.run()

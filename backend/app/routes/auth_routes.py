from flask import Blueprint, request, jsonify, redirect, url_for, session
from app.models.user import User
from app import db
import jwt
import datetime
from flask import current_app
from authlib.integrations.flask_client import OAuth

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={'scope': 'openid email profile'}
    )

@auth_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'msg': 'auth ok'})

#register page
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already exists'}), 400
    user = User(
        first_name=data.get('firstName'),
        last_name=data.get('lastName'),
        company_name=data.get('companyName'),
        email=data.get('email'),
        role=data.get('role')
    )
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        token = jwt.encode({
            'user_id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'message': 'Login successful', 'token': token, 'role': user.role}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/google-login')
def google_login():
    role = request.args.get('role')
    if role:
        session['google_role'] = role
    redirect_uri = url_for('auth.google_auth_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/google-auth-callback')
def google_auth_callback():
    token = oauth.google.authorize_access_token()
    userinfo = oauth.google.parse_id_token(token)
    email = userinfo['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        # New user, ask for role selection (frontend should handle this)
        session['google_email'] = email
        session['google_name'] = userinfo.get('name', '')
        return redirect('/select-role')  # Frontend route to select role
    # Existing user, login
    jwt_token = jwt.encode({
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return redirect(f'/google-auth-success?token={jwt_token}&role={user.role}')

@auth_bp.route('/google-register', methods=['POST'])
def google_register():
    data = request.json
    email = session.get('google_email')
    name = session.get('google_name')
    role = session.get('google_role')
    if not email or not role:
        return jsonify({'error': 'Missing data'}), 400
    user = User(
        first_name=name.split(' ')[0],
        last_name=' '.join(name.split(' ')[1:]),
        company_name='',
        email=email,
        role=role
    )
    user.set_password('')  # No password for Google users
    db.session.add(user)
    db.session.commit()
    jwt_token = jwt.encode({
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'message': 'Google registration successful', 'token': jwt_token, 'role': user.role}), 201
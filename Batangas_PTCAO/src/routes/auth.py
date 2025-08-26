from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from flask_jwt_extended import create_access_token, set_access_cookies
from extension import db, bcrypt
from model import User
from enum import Enum

# Create blueprint
auth_bp = Blueprint('auth', __name__)

class AccountStatus(Enum):
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    MAINTENANCE = 'maintenance'

# Built-in admin account credentials
ADMIN_EMAIL = "admin@ptcao.gov.ph"
ADMIN_PASSWORD = "Admin@1234"
PTCAO_EMAIL = "ptcao@ptcao.gov.ph"
PTCAO_PASSWORD = "Ptcao@1234"

@auth_bp.route('/')
def home():
    return render_template('Login.html')

@auth_bp.route('/tourist')
def tourist_home():
    return render_template('TOURIST_Home.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('Login.html')

        # Check for built-in admin account
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            # Create a dummy admin user object
            admin_user = type('obj', (object,), {
                'user_id': 'admin',
                'is_active': True,
                'check_password': lambda x: x == ADMIN_PASSWORD
            })

            access_token = create_access_token(identity="admin")
            session['user_id'] = "admin"
            session['user_role'] = "admin"
            session['is_logged_in'] = True
            
            # Create response with JWT cookie
            response = make_response(redirect(url_for('admin_dashboard.admin_dashboard')))
            set_access_cookies(response, access_token)
            return response

        # Check for built-in PTCAO account
        if email == PTCAO_EMAIL and password == PTCAO_PASSWORD:
            admin_user = type('obj', (object,), {
                'user_id': 'ptcao',
                'is_active': True,
                'check_password': lambda x: x == PTCAO_PASSWORD
            })

            access_token = create_access_token(identity="ptcao")
            session['user_id'] = "ptcao"
            session['user_role'] = "ptcao"
            session['is_logged_in'] = True
            
            # Create response with JWT cookie
            response = make_response(redirect(url_for('ptcao_dashboard.ptcao_dashboard')))
            set_access_cookies(response, access_token)
            return response

        # Check database users
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account is not active. Please contact an administrator.', 'error')
                return render_template('Login.html')

            access_token = create_access_token(identity=user.user_id)
            session['user_id'] = user.user_id
            session['user_role'] = user.designation.lower()
            session['is_logged_in'] = True
            session['municipality'] = user.municipality

            # Create response with JWT cookie
            if user.designation.lower() == 'admin':
                response = make_response(redirect(url_for('admin_dashboard.admin_dashboard')))
            elif user.designation.lower() == 'mto':
                response = make_response(redirect(url_for('dashboard.mto_dashboard')))
            elif user.designation.lower() == 'ptcao':
                response = make_response(redirect(url_for('ptcao_dashboard.ptcao_dashboard')))
            else:
                response = make_response(redirect(url_for('dashboard.mto_dashboard')))
            
            set_access_cookies(response, access_token)
            return response
        else:
            flash('Invalid email or password', 'error')
            return render_template('Login.html')

    return render_template('Login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect(url_for('auth.home')))
    # Clear JWT cookies
    response.set_cookie('access_token_cookie', '', expires=0)
    flash('You have been logged out successfully', 'success')
    return response

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name', '').strip()
        municipality = request.form.get('municipality', '').strip()
        id_number = request.form.get('id_number', '').strip()
        designation = request.form.get('designation', '').strip()
        email = request.form.get('email', '').strip().lower()
        gender = request.form.get('gender', '').strip()
        birthday = request.form.get('birthday', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Basic validation
        if not all([full_name, municipality, id_number, designation, email, gender, birthday, username, password]):
            flash('All fields are required', 'error')
            return render_template('Register.html')

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('Register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return render_template('Register.html')

        # Create new user
        try:
            from datetime import datetime
            birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
            
            new_user = User(
                full_name=full_name,
                municipality=municipality,
                id_number=id_number,
                designation=designation,
                email=email,
                gender=gender,
                birthday=birthday_date,
                username=username,
                is_active=False  # Requires admin activation
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please wait for admin approval.', 'success')
            return redirect(url_for('auth.home'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('Register.html')

    return render_template('Register.html')

def init_auth_routes(app):
    """Legacy function for compatibility"""
    pass
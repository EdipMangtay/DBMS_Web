from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from services.auth_service import AuthService
from wtforms import Form, StringField, PasswordField, validators

auth_bp = Blueprint('auth', __name__)

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=3, max=50)])
    password = PasswordField('Password', [validators.DataRequired()])

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return redirect(url_for('auth.login_selector'))

@auth_bp.route('/login/select', methods=['GET'])
def login_selector():
    if current_user.is_authenticated:
        if current_user.role == 'Admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'Instructor':
            return redirect(url_for('instructor.dashboard'))
        elif current_user.role == 'Student':
            return redirect(url_for('student.dashboard'))
    return render_template('auth/login_selector.html')

@auth_bp.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated:
        if current_user.role == 'Student':
            return redirect(url_for('student.dashboard'))
        else:
            old_role = current_user.role
            logout_user()
            from flask import session
            session.clear()
            session.pop('_user_id', None)
            session.pop('_fresh', None)
            flash(f'Logged out from {old_role} account. Please login as Student.', 'info')
    
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            flash('Please fill in all fields correctly', 'danger')
            return render_template('auth/student_login.html', form=form)
        
        username = form.username.data.strip()
        password = form.password.data
        
        user = AuthService.authenticate(username, password, 'Student')
        if user:
            if user.role != 'Student':
                user.role = 'Student'
                from database import db
                db.session.commit()
            from flask import session
            session.clear()
            login_user(user, remember=False)
            next_page = request.args.get('next') or url_for('student.dashboard')
            return redirect(next_page)
        else:
            flash('Invalid username or password. Use: edip / edip123', 'danger')
    
    return render_template('auth/student_login.html', form=form)

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.role == 'Admin':
            return redirect(url_for('admin.dashboard'))
        else:
            old_role = current_user.role
            logout_user()
            from flask import session
            session.clear()
            session.pop('_user_id', None)
            session.pop('_fresh', None)
            flash(f'Logged out from {old_role} account. Please login as Admin.', 'info')
    
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            flash('Please fill in all fields correctly', 'danger')
            return render_template('auth/admin_login.html', form=form)
        
        username = form.username.data.strip()
        password = form.password.data
        
        user = AuthService.authenticate(username, password, 'Admin')
        if user:
            if user.role != 'Admin':
                user.role = 'Admin'
                from database import db
                db.session.commit()
            from flask import session
            session.clear()
            login_user(user, remember=False)
            next_page = request.args.get('next') or url_for('admin.dashboard')
            return redirect(next_page)
        else:
            flash('Invalid username or password. Use: edip / edip123', 'danger')
    
    return render_template('auth/admin_login.html', form=form)

@auth_bp.route('/instructor/login', methods=['GET', 'POST'])
def instructor_login():
    if current_user.is_authenticated:
        if current_user.role == 'Instructor':
            return redirect(url_for('instructor.dashboard'))
        else:
            old_role = current_user.role
            logout_user()
            from flask import session
            session.clear()
            session.pop('_user_id', None)
            session.pop('_fresh', None)
            flash(f'Logged out from {old_role} account. Please login as Instructor.', 'info')
    
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            flash('Please fill in all fields correctly', 'danger')
            return render_template('auth/instructor_login.html', form=form)
        
        username = form.username.data.strip()
        password = form.password.data
        
        user = AuthService.authenticate(username, password, 'Instructor')
        if user:
            if user.role != 'Instructor':
                user.role = 'Instructor'
                from database import db
                db.session.commit()
            from flask import session
            session.clear()
            login_user(user, remember=False)
            next_page = request.args.get('next') or url_for('instructor.dashboard')
            return redirect(next_page)
        else:
            flash('Invalid username or password. Use: edip / edip123', 'danger')
    
    return render_template('auth/instructor_login.html', form=form)

@auth_bp.route('/logout')
def logout():
    from flask import session, make_response, redirect as flask_redirect, url_for
    
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out', 'info')
    
    session.clear()
    session.pop('_user_id', None)
    session.pop('_fresh', None)
    session.pop('_remember', None)
    session.pop('_remember_seconds', None)
    
    response = make_response(flask_redirect(url_for('auth.login_selector')))
    
    response.set_cookie('remember_token', '', expires=0, max_age=0, path='/')
    response.set_cookie('session', '', expires=0, max_age=0, path='/')
    response.set_cookie('_remember_me', '', expires=0, max_age=0, path='/')
    
    return response





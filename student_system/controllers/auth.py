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
    
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = AuthService.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user, remember=True)
            next_page = request.args.get('next')
            if not next_page:
                if user.role == 'Admin':
                    next_page = url_for('admin.dashboard')
                elif user.role == 'Instructor':
                    next_page = url_for('instructor.dashboard')
                elif user.role == 'Student':
                    next_page = url_for('student.dashboard')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))





import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_login import LoginManager
from config import Config
from database import db
from models import User
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.instructor import instructor_bp
from controllers.student import student_bp
from controllers.reports import reports_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Setup logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/student_system.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Student System startup')
    
    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(instructor_bp, url_prefix='/instructor')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    # Root route
    @app.route('/')
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        if current_user.is_authenticated:
            if current_user.role == 'Admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'Instructor':
                return redirect(url_for('instructor.dashboard'))
            elif current_user.role == 'Student':
                return redirect(url_for('student.dashboard'))
        return redirect(url_for('auth.login'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


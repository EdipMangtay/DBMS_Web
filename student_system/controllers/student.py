from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from services.student_service import StudentService
from repositories import StudentRepository

student_bp = Blueprint('student', __name__)

def student_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'Student':
            flash('Access denied. Student privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@student_required
def dashboard():
    from models import Student, User
    from database import db
    
    student = None
    if current_user.user_id:
        student = db.session.query(Student).filter_by(user_id=current_user.user_id).first()
    
    if not student:
        user = db.session.query(User).filter_by(username=current_user.username).first()
        if user and user.user_id:
            student = db.session.query(Student).filter_by(user_id=user.user_id).first()
    
    if not student:
        flash('Student profile not found. Please contact administrator.', 'danger')
        return redirect(url_for('auth.logout'))
    
    page = request.args.get('page', 1, type=int)
    pagination = StudentService.get_student_enrollments(student.student_id, page, 20)
    
    overall_avg = StudentService.get_overall_average(student.student_id)
    
    from repositories.grade_repository import GradeRepository
    enrollment_averages = {}
    for enrollment in pagination.items:
        avg = GradeRepository.calculate_enrollment_average(enrollment.enrollment_id)
        enrollment_averages[enrollment.enrollment_id] = avg
    
    return render_template('student/dashboard.html', 
                         enrollments=pagination.items, 
                         pagination=pagination,
                         overall_avg=overall_avg,
                         enrollment_averages=enrollment_averages)

@student_bp.route('/transcript')
@student_required
def transcript():
    student = StudentRepository.get_by_user_id(current_user.user_id) if current_user.user_id else None
    if not student:
        student = StudentRepository.get_by_user_email(current_user.username) if current_user.username else None
    
    if not student and (current_user.username == 'edip_student' or current_user.username.startswith('edip')):
        from database import db
        student = StudentRepository.create(
            user_id=current_user.user_id,
            first_name='Edip',
            last_name='Student',
            email='edip@student.local'
        )
    
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('auth.logout'))
    
    transcript_details = StudentService.get_transcript_details(student.student_id)
    overall_avg = StudentService.get_overall_average(student.student_id)
    
    return render_template('student/transcript.html', 
                         transcript=transcript_details,
                         overall_avg=overall_avg)

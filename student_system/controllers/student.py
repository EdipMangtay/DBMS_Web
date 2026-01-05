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
    # Get student by username (which is email) from user
    student = StudentRepository.get_by_user_email(current_user.username) if current_user.username else None
    if not student:
        flash('Student profile not found. Please contact administrator.', 'danger')
        return redirect(url_for('auth.logout'))
    
    page = request.args.get('page', 1, type=int)
    pagination = StudentService.get_student_enrollments(student.student_id, page, 20)
    
    # Get overall average
    overall_avg = StudentService.get_overall_average(student.student_id)
    
    return render_template('student/dashboard.html', 
                         enrollments=pagination.items, 
                         pagination=pagination,
                         overall_avg=overall_avg)

@student_bp.route('/transcript')
@student_required
def transcript():
    student = StudentRepository.get_by_user_email(current_user.username) if current_user.username else None
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('auth.logout'))
    
    transcript_details = StudentService.get_transcript_details(student.student_id)
    overall_avg = StudentService.get_overall_average(student.student_id)
    
    return render_template('student/transcript.html', 
                         transcript=transcript_details,
                         overall_avg=overall_avg)

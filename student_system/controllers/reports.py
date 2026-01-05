from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from services.report_service import ReportService
from repositories import StudentRepository

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/course-performance')
@login_required
def course_performance():
    if current_user.role not in ['Admin', 'Instructor']:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    report = ReportService.get_course_performance_report()
    return render_template('reports/course_performance.html', report=report)

@reports_bp.route('/student-transcript/<int:student_id>')
@login_required
def student_transcript(student_id):
    if current_user.role == 'Student':
        student = StudentRepository.get_by_user_email(current_user.username) if current_user.username else None
        if not student or student.student_id != student_id:
            flash('Access denied', 'danger')
            return redirect(url_for('index'))
    
    transcript_details = ReportService.get_student_transcript_details(student_id)
    student = StudentRepository.get_by_id(student_id)
    overall_avg = None
    if student:
        from services.student_service import StudentService
        overall_avg = StudentService.get_overall_average(student_id)
    
    return render_template('reports/student_transcript.html', 
                         transcript=transcript_details,
                         student=student,
                         overall_avg=overall_avg)

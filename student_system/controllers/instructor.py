from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from services.instructor_service import InstructorService
from repositories import InstructorRepository, GradeRepository, AssessmentTypeRepository
from wtforms import Form, StringField, DecimalField, SelectField, validators

instructor_bp = Blueprint('instructor', __name__)

def instructor_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'Instructor':
            flash('Access denied. Instructor privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

class GradeForm(Form):
    assessment_type_id = SelectField('Assessment Type', [validators.DataRequired()], choices=[])
    score = DecimalField('Score', [validators.DataRequired(), validators.NumberRange(min=0, max=100)])

@instructor_bp.route('/dashboard')
@instructor_required
def dashboard():
    # Get instructor by username (which is email) from user
    instructor = InstructorRepository.get_by_user_email(current_user.username) if current_user.username else None
    if not instructor:
        flash('Instructor profile not found. Please contact administrator.', 'danger')
        return redirect(url_for('auth.logout'))
    
    page = request.args.get('page', 1, type=int)
    pagination = InstructorService.get_instructor_sections(instructor.instructor_id, page, 20)
    return render_template('instructor/dashboard.html', sections=pagination.items, pagination=pagination)

@instructor_bp.route('/sections/<int:section_id>')
@instructor_required
def view_section(section_id):
    instructor = InstructorRepository.get_by_user_email(current_user.username) if current_user.username else None
    if not instructor:
        flash('Instructor profile not found', 'danger')
        return redirect(url_for('auth.logout'))
    
    from repositories import SectionRepository
    section = SectionRepository.get_by_id(section_id)
    
    if not section or section.instructor_id != instructor.instructor_id:
        flash('Section not found or access denied', 'danger')
        return redirect(url_for('instructor.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    pagination = InstructorService.get_section_enrollments(section_id, page, 50)
    
    # Get statistics
    stats = InstructorService.get_section_statistics(section_id)
    
    return render_template('instructor/section.html', section=section, enrollments=pagination.items, pagination=pagination, stats=stats)

@instructor_bp.route('/sections/<int:section_id>/statistics')
@instructor_required
def section_statistics(section_id):
    instructor = InstructorRepository.get_by_user_email(current_user.username) if current_user.username else None
    if not instructor:
        flash('Instructor profile not found', 'danger')
        return redirect(url_for('auth.logout'))
    
    from repositories import SectionRepository
    section = SectionRepository.get_by_id(section_id)
    
    if not section or section.instructor_id != instructor.instructor_id:
        flash('Section not found or access denied', 'danger')
        return redirect(url_for('instructor.dashboard'))
    
    stats = InstructorService.get_section_statistics(section_id)
    course_stats = InstructorService.get_course_statistics(section.course_id)
    
    return render_template('instructor/statistics.html', section=section, section_stats=stats, course_stats=course_stats)

@instructor_bp.route('/enrollments/<int:enrollment_id>/grades', methods=['GET', 'POST'])
@instructor_required
def manage_grades(enrollment_id):
    instructor = InstructorRepository.get_by_user_email(current_user.username) if current_user.username else None
    if not instructor:
        flash('Instructor profile not found', 'danger')
        return redirect(url_for('auth.logout'))
    
    from repositories import EnrollmentRepository
    enrollment = EnrollmentRepository.get_by_id(enrollment_id)
    
    if not enrollment or enrollment.section.instructor_id != instructor.instructor_id:
        flash('Enrollment not found or access denied', 'danger')
        return redirect(url_for('instructor.dashboard'))
    
    grades = GradeRepository.get_by_enrollment(enrollment_id)
    form = GradeForm(request.form)
    
    # Populate assessment type choices
    assessment_types = AssessmentTypeRepository.get_all()
    form.assessment_type_id.choices = [(str(at.assessment_type_id), f"{at.type_name} ({at.weight}%)") for at in assessment_types]
    
    if request.method == 'POST' and form.validate():
        try:
            InstructorService.enter_grade(
                enrollment_id,
                int(form.assessment_type_id.data),
                float(form.score.data)
            )
            flash('Grade entered successfully', 'success')
            return redirect(url_for('instructor.manage_grades', enrollment_id=enrollment_id))
        except Exception as e:
            flash(f'Error entering grade: {str(e)}', 'danger')
    
    return render_template('instructor/grades.html', enrollment=enrollment, grades=grades, form=form)

@instructor_bp.route('/grades/<int:grade_id>/edit', methods=['GET', 'POST'])
@instructor_required
def edit_grade(grade_id):
    instructor = InstructorRepository.get_by_user_email(current_user.username) if current_user.username else None
    if not instructor:
        flash('Instructor profile not found', 'danger')
        return redirect(url_for('auth.logout'))
    
    grade = GradeRepository.get_by_id(grade_id)
    
    if not grade or grade.enrollment.section.instructor_id != instructor.instructor_id:
        flash('Grade not found or access denied', 'danger')
        return redirect(url_for('instructor.dashboard'))
    
    form = GradeForm(request.form)
    
    # Populate assessment type choices
    assessment_types = AssessmentTypeRepository.get_all()
    form.assessment_type_id.choices = [(str(at.assessment_type_id), f"{at.type_name} ({at.weight}%)") for at in assessment_types]
    form.assessment_type_id.data = str(grade.assessment_type_id)
    
    if request.method == 'POST' and form.validate():
        try:
            InstructorService.update_grade(
                grade_id,
                score=float(form.score.data)
            )
            flash('Grade updated successfully', 'success')
            return redirect(url_for('instructor.manage_grades', enrollment_id=grade.enrollment_id))
        except Exception as e:
            flash(f'Error updating grade: {str(e)}', 'danger')
    
    form.score.data = grade.score
    return render_template('instructor/grade_form.html', form=form, grade=grade)

@instructor_bp.route('/grades/<int:grade_id>/delete', methods=['POST'])
@instructor_required
def delete_grade(grade_id):
    instructor = InstructorRepository.get_by_user_email(current_user.username) if current_user.username else None
    if not instructor:
        flash('Instructor profile not found', 'danger')
        return redirect(url_for('auth.logout'))
    
    grade = GradeRepository.get_by_id(grade_id)
    
    if not grade or grade.enrollment.section.instructor_id != instructor.instructor_id:
        flash('Grade not found or access denied', 'danger')
        return redirect(url_for('instructor.dashboard'))
    
    enrollment_id = grade.enrollment_id
    try:
        GradeRepository.delete(grade_id)
        flash('Grade deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting grade: {str(e)}', 'danger')
    
    return redirect(url_for('instructor.manage_grades', enrollment_id=enrollment_id))

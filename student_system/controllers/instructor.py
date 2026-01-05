from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from services.instructor_service import InstructorService
from repositories import InstructorRepository, GradeRepository
from wtforms import Form, StringField, DecimalField, TextAreaField, validators

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
    assessment_type = StringField('Assessment Type', [validators.DataRequired(), validators.Length(min=1, max=50)])
    score = DecimalField('Score', [validators.DataRequired(), validators.NumberRange(min=0, max=100)])
    max_score = DecimalField('Max Score', [validators.Optional()], default=100.00)
    weight = DecimalField('Weight', [validators.Optional()], description='Weight as decimal (e.g., 0.30 for 30%)')
    notes = TextAreaField('Notes', [validators.Optional()])

@instructor_bp.route('/dashboard')
@instructor_required
def dashboard():
    from models import Instructor, User
    from database import db
    
    instructor = None
    if current_user.user_id:
        instructor = db.session.query(Instructor).filter_by(user_id=current_user.user_id).first()
    
    if not instructor:
        user = db.session.query(User).filter_by(username=current_user.username).first()
        if user and user.user_id:
            instructor = db.session.query(Instructor).filter_by(user_id=user.user_id).first()
    
    if not instructor:
        flash('Instructor profile not found. Please contact administrator.', 'danger')
        return redirect(url_for('auth.logout'))
    
    page = request.args.get('page', 1, type=int)
    pagination = InstructorService.get_instructor_sections(instructor.instructor_id, page, 20)
    return render_template('instructor/dashboard.html', sections=pagination.items, pagination=pagination)

@instructor_bp.route('/sections/<int:section_id>')
@instructor_required
def view_section(section_id):
    from models import Instructor, User
    from database import db
    
    instructor = None
    if current_user.user_id:
        instructor = db.session.query(Instructor).filter_by(user_id=current_user.user_id).first()
    
    if not instructor:
        user = db.session.query(User).filter_by(username=current_user.username).first()
        if user and user.user_id:
            instructor = db.session.query(Instructor).filter_by(user_id=user.user_id).first()
    if not instructor and (current_user.username == 'edip_instructor' or current_user.username.startswith('edip')):
        from database import db
        instructor = InstructorRepository.create(
            user_id=current_user.user_id,
            first_name='Admin',
            last_name='Instructor',
            email='admin@instructor.local'
        )
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
    
    stats = InstructorService.get_section_statistics(section_id)
    
    return render_template('instructor/section.html', section=section, enrollments=pagination.items, pagination=pagination, stats=stats)

@instructor_bp.route('/sections/<int:section_id>/statistics')
@instructor_required
def section_statistics(section_id):
    from models import Instructor, User
    from database import db
    
    instructor = None
    if current_user.user_id:
        instructor = db.session.query(Instructor).filter_by(user_id=current_user.user_id).first()
    
    if not instructor:
        user = db.session.query(User).filter_by(username=current_user.username).first()
        if user and user.user_id:
            instructor = db.session.query(Instructor).filter_by(user_id=user.user_id).first()
    if not instructor and (current_user.username == 'edip_instructor' or current_user.username.startswith('edip')):
        from database import db
        instructor = InstructorRepository.create(
            user_id=current_user.user_id,
            first_name='Admin',
            last_name='Instructor',
            email='admin@instructor.local'
        )
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
    from models import Instructor, User
    from database import db
    
    instructor = None
    if current_user.user_id:
        instructor = db.session.query(Instructor).filter_by(user_id=current_user.user_id).first()
    
    if not instructor:
        user = db.session.query(User).filter_by(username=current_user.username).first()
        if user and user.user_id:
            instructor = db.session.query(Instructor).filter_by(user_id=user.user_id).first()
    if not instructor and (current_user.username == 'edip_instructor' or current_user.username.startswith('edip')):
        from database import db
        instructor = InstructorRepository.create(
            user_id=current_user.user_id,
            first_name='Admin',
            last_name='Instructor',
            email='admin@instructor.local'
        )
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
    
    if request.method == 'POST' and form.validate():
        try:
            assessment_type = form.assessment_type.data.strip()
            score = float(form.score.data)
            max_score = float(form.max_score.data) if form.max_score.data else 100.00
            
            weight_input = form.weight.data
            if weight_input:
                weight_value = float(weight_input)
                if weight_value > 1:
                    weight = weight_value / 100.0
                else:
                    weight = weight_value
            else:
                weight = None
            
            notes = form.notes.data.strip() if form.notes.data else None
            
            existing_grade = GradeRepository.get_by_assessment_type_name(enrollment_id, assessment_type)
            if existing_grade:
                GradeRepository.update(existing_grade.grade_id, 
                                     score=score, 
                                     max_score=max_score, 
                                     weight=weight,
                                     notes=notes)
                flash('Grade updated successfully', 'success')
            else:
                GradeRepository.create_grade(
                    enrollment_id=enrollment_id,
                    assessment_type=assessment_type,
                    score=score,
                    max_score=max_score,
                    weight=weight,
                    notes=notes
                )
                flash('Grade entered successfully', 'success')
            return redirect(url_for('instructor.manage_grades', enrollment_id=enrollment_id))
        except Exception as e:
            flash(f'Error entering grade: {str(e)}', 'danger')
    
    return render_template('instructor/grades.html', enrollment=enrollment, grades=grades, form=form)

@instructor_bp.route('/grades/<int:grade_id>/edit', methods=['GET', 'POST'])
@instructor_required
def edit_grade(grade_id):
    from models import Instructor, User
    from database import db
    
    instructor = None
    if current_user.user_id:
        instructor = db.session.query(Instructor).filter_by(user_id=current_user.user_id).first()
    
    if not instructor:
        user = db.session.query(User).filter_by(username=current_user.username).first()
        if user and user.user_id:
            instructor = db.session.query(Instructor).filter_by(user_id=user.user_id).first()
    if not instructor and (current_user.username == 'edip_instructor' or current_user.username.startswith('edip')):
        from database import db
        instructor = InstructorRepository.create(
            user_id=current_user.user_id,
            first_name='Admin',
            last_name='Instructor',
            email='admin@instructor.local'
        )
    if not instructor:
        flash('Instructor profile not found', 'danger')
        return redirect(url_for('auth.logout'))
    
    grade = GradeRepository.get_by_id(grade_id)
    
    if not grade or grade.enrollment.section.instructor_id != instructor.instructor_id:
        flash('Grade not found or access denied', 'danger')
        return redirect(url_for('instructor.dashboard'))
    
    form = GradeForm(request.form)
    
    if request.method == 'POST' and form.validate():
        try:
            max_score = float(form.max_score.data) if form.max_score.data else grade.max_score
            
            # Weight: if user enters percentage (e.g., 30), convert to decimal (0.30)
            weight_input = form.weight.data
            if weight_input:
                weight_value = float(weight_input)
                if weight_value > 1:
                    weight = weight_value / 100.0
                else:
                    weight = weight_value
            else:
                weight = grade.weight
            
            notes = form.notes.data.strip() if form.notes.data else grade.notes
            
            GradeRepository.update(grade_id,
                                 score=float(form.score.data),
                                 max_score=max_score,
                                 weight=weight,
                                 notes=notes)
            flash('Grade updated successfully', 'success')
            return redirect(url_for('instructor.manage_grades', enrollment_id=grade.enrollment_id))
        except Exception as e:
            flash(f'Error updating grade: {str(e)}', 'danger')
    
    form.assessment_type.data = grade.assessment_type
    form.score.data = grade.score
    form.max_score.data = grade.max_score if grade.max_score else 100.00
    form.weight.data = grade.weight if grade.weight else None
    form.notes.data = grade.notes if grade.notes else None
    return render_template('instructor/grade_form.html', form=form, grade=grade)

@instructor_bp.route('/grades/<int:grade_id>/delete', methods=['POST'])
@instructor_required
def delete_grade(grade_id):
    from models import Instructor, User
    from database import db
    
    instructor = None
    if current_user.user_id:
        instructor = db.session.query(Instructor).filter_by(user_id=current_user.user_id).first()
    
    if not instructor:
        user = db.session.query(User).filter_by(username=current_user.username).first()
        if user and user.user_id:
            instructor = db.session.query(Instructor).filter_by(user_id=user.user_id).first()
    if not instructor and (current_user.username == 'edip_instructor' or current_user.username.startswith('edip')):
        from database import db
        instructor = InstructorRepository.create(
            user_id=current_user.user_id,
            first_name='Admin',
            last_name='Instructor',
            email='admin@instructor.local'
        )
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

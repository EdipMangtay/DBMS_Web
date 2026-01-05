from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from services.admin_service import AdminService
from repositories import CourseRepository, SemesterRepository, SectionRepository, StudentRepository, InstructorRepository
from wtforms import Form, StringField, IntegerField, DateField, SelectField, TextAreaField, validators
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

class StudentForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=3, max=50)])
    password = StringField('Password', [validators.DataRequired(), validators.Length(min=6)])
    student_name = StringField('Student Name', [validators.DataRequired()])
    student_mail = StringField('Email', [validators.DataRequired(), validators.Email()])

class InstructorForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=3, max=50)])
    password = StringField('Password', [validators.DataRequired(), validators.Length(min=6)])
    full_name = StringField('Full Name', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])

class CourseForm(Form):
    course_name = StringField('Course Name', [validators.DataRequired()])
    department = StringField('Department', [validators.Optional()])  # String, not foreign key
    course_code = StringField('Course Code', [validators.DataRequired()])
    credits = IntegerField('Credits', [validators.DataRequired(), validators.NumberRange(min=1, max=6)], default=3)
    description = TextAreaField('Description', [validators.Optional()])

class SemesterForm(Form):
    term_name = StringField('Term Name', [validators.DataRequired()], description='e.g., Fall 2025')
    start_date = DateField('Start Date', [validators.DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', [validators.DataRequired()], format='%Y-%m-%d')

class SectionForm(Form):
    course_id = SelectField('Course', [validators.DataRequired()], choices=[])
    instructor_id = SelectField('Instructor', [validators.DataRequired()], choices=[])
    semester_id = SelectField('Semester', [validators.DataRequired()], choices=[])
    section_code = StringField('Section Code', [validators.DataRequired()], description='e.g., A, B, LAB1')
    room = StringField('Room', [validators.Optional()])
    schedule_text = StringField('Schedule', [validators.Optional()], description='e.g., Mon 10:00-12:00')

class EnrollmentForm(Form):
    student_id = SelectField('Student', [validators.DataRequired()], choices=[])
    section_id = SelectField('Section', [validators.DataRequired()], choices=[])

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    from models import Student, Instructor, Course, Enrollment
    
    total_students = Student.query.count()
    total_instructors = Instructor.query.count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    
    return render_template('admin/dashboard.html', 
                         total_students=total_students,
                         total_instructors=total_instructors,
                         total_courses=total_courses,
                         total_enrollments=total_enrollments)

@admin_bp.route('/students')
@admin_required
def students():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    pagination = AdminService.get_students(page, 20, search if search else None)
    return render_template('admin/students.html', students=pagination.items, pagination=pagination, search=search)

@admin_bp.route('/students/create', methods=['GET', 'POST'])
@admin_required
def create_student():
    form = StudentForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            AdminService.create_student(
                form.username.data,
                form.password.data,
                form.student_name.data,
                form.student_mail.data
            )
            flash('Student created successfully', 'success')
            return redirect(url_for('admin.students'))
        except Exception as e:
            flash(f'Error creating student: {str(e)}', 'danger')
    return render_template('admin/student_form.html', form=form, title='Create Student')

@admin_bp.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_student(student_id):
    student = StudentRepository.get_by_id(student_id)
    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('admin.students'))
    
    form = StudentForm(request.form, obj=student)
    if request.method == 'POST' and form.validate():
        try:
            AdminService.update_student(
                student_id,
                student_name=form.student_name.data,
                student_mail=form.student_mail.data
            )
            flash('Student updated successfully', 'success')
            return redirect(url_for('admin.students'))
        except Exception as e:
            flash(f'Error updating student: {str(e)}', 'danger')
    
    return render_template('admin/student_form.html', form=form, student=student, title='Edit Student')

@admin_bp.route('/students/<int:student_id>/delete', methods=['POST'])
@admin_required
def delete_student(student_id):
    try:
        AdminService.delete_student(student_id)
        flash('Student deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'danger')
    return redirect(url_for('admin.students'))

@admin_bp.route('/instructors')
@admin_required
def instructors():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    pagination = AdminService.get_instructors(page, 20, search if search else None)
    return render_template('admin/instructors.html', instructors=pagination.items, pagination=pagination, search=search)

@admin_bp.route('/instructors/create', methods=['GET', 'POST'])
@admin_required
def create_instructor():
    form = InstructorForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            AdminService.create_instructor(
                form.username.data,
                form.password.data,
                form.full_name.data,
                form.email.data
            )
            flash('Instructor created successfully', 'success')
            return redirect(url_for('admin.instructors'))
        except Exception as e:
            flash(f'Error creating instructor: {str(e)}', 'danger')
    return render_template('admin/instructor_form.html', form=form, title='Create Instructor')

@admin_bp.route('/instructors/<int:instructor_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_instructor(instructor_id):
    instructor = InstructorRepository.get_by_id(instructor_id)
    if not instructor:
        flash('Instructor not found', 'danger')
        return redirect(url_for('admin.instructors'))
    
    form = InstructorForm(request.form, obj=instructor)
    
    if request.method == 'POST' and form.validate():
        try:
            AdminService.update_instructor(
                instructor_id,
                full_name=form.full_name.data,
                email=form.email.data
            )
            flash('Instructor updated successfully', 'success')
            return redirect(url_for('admin.instructors'))
        except Exception as e:
            flash(f'Error updating instructor: {str(e)}', 'danger')
    
    return render_template('admin/instructor_form.html', form=form, instructor=instructor, title='Edit Instructor')

@admin_bp.route('/instructors/<int:instructor_id>/delete', methods=['POST'])
@admin_required
def delete_instructor(instructor_id):
    try:
        AdminService.delete_instructor(instructor_id)
        flash('Instructor deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting instructor: {str(e)}', 'danger')
    return redirect(url_for('admin.instructors'))

@admin_bp.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    pagination = AdminService.get_courses(page, 20, search if search else None)
    return render_template('admin/courses.html', courses=pagination.items, pagination=pagination, search=search)

@admin_bp.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm(request.form)
    
    if request.method == 'POST' and form.validate():
        try:
            AdminService.create_course(
                course_name=form.course_name.data,
                course_code=form.course_code.data,
                department=form.department.data,
                credits=form.credits.data,
                description=form.description.data
            )
            flash('Course created successfully', 'success')
            return redirect(url_for('admin.courses'))
        except Exception as e:
            flash(f'Error creating course: {str(e)}', 'danger')
    return render_template('admin/course_form.html', form=form, title='Create Course')

@admin_bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = CourseRepository.get_by_id(course_id)
    if not course:
        flash('Course not found', 'danger')
        return redirect(url_for('admin.courses'))
    
    form = CourseForm(request.form, obj=course)
    
    if not form.course_code.data and course:
        form.course_code.data = course.course_code
    if not form.credits.data and course:
        form.credits.data = course.credits
    if not form.description.data and course:
        form.description.data = course.description
    
    if request.method == 'POST' and form.validate():
        try:
            AdminService.update_course(
                course_id,
                course_name=form.course_name.data,
                course_code=form.course_code.data,
                department=form.department.data,
                credits=form.credits.data,
                description=form.description.data
            )
            flash('Course updated successfully', 'success')
            return redirect(url_for('admin.courses'))
        except Exception as e:
            flash(f'Error updating course: {str(e)}', 'danger')
    
    return render_template('admin/course_form.html', form=form, course=course, title='Edit Course')

@admin_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
@admin_required
def delete_course(course_id):
    try:
        AdminService.delete_course(course_id)
        flash('Course deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting course: {str(e)}', 'danger')
    return redirect(url_for('admin.courses'))

@admin_bp.route('/semesters/create', methods=['GET', 'POST'])
@admin_required
def create_semester():
    form = SemesterForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            AdminService.create_semester(
                form.term_name.data,
                form.start_date.data,
                form.end_date.data
            )
            flash('Semester created successfully', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            flash(f'Error creating semester: {str(e)}', 'danger')
    return render_template('admin/semester_form.html', form=form, title='Create Semester')

@admin_bp.route('/sections/create', methods=['GET', 'POST'])
@admin_required
def create_section():
    form = SectionForm(request.form)
    courses = CourseRepository.get_all(page=1, per_page=1000)
    form.course_id.choices = [(str(c.course_id), f"{c.course_name}") for c in courses.items]
    
    instructors = InstructorRepository.get_all(page=1, per_page=1000)
    form.instructor_id.choices = [(str(i.instructor_id), i.full_name) for i in instructors.items]
    
    semesters = SemesterRepository.get_all()
    form.semester_id.choices = [(str(s.semester_id), s.term_name) for s in semesters]
    
    if request.method == 'POST' and form.validate():
        try:
            AdminService.create_section(
                int(form.course_id.data),
                int(form.instructor_id.data),
                int(form.semester_id.data),
                form.section_code.data,
                form.room.data or None,
                form.schedule_text.data or None
            )
            flash('Section created successfully', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            flash(f'Error creating section: {str(e)}', 'danger')
    return render_template('admin/section_form.html', form=form, title='Create Section')

@admin_bp.route('/enrollments/create', methods=['GET', 'POST'])
@admin_required
def create_enrollment():
    form = EnrollmentForm(request.form)
    
    students = StudentRepository.get_all(page=1, per_page=1000)
    form.student_id.choices = [(str(s.student_id), f"{s.student_name} ({s.student_mail})") for s in students.items]
    
    sections = SectionRepository.get_all(page=1, per_page=1000)
    form.section_id.choices = [(str(s.section_id), f"{s.course.course_name} - {s.section_code} ({s.semester.term_name})") for s in sections.items]
    
    if request.method == 'POST' and form.validate():
        try:
            enrollment, error = AdminService.enroll_student(int(form.student_id.data), int(form.section_id.data))
            if error:
                flash(error, 'danger')
            else:
                flash('Student enrolled successfully', 'success')
                return redirect(url_for('admin.dashboard'))
        except Exception as e:
            flash(f'Error enrolling student: {str(e)}', 'danger')
    return render_template('admin/enrollment_form.html', form=form, title='Enroll Student')

"""
Script to create sample data for edip_student user.
This will create courses, sections, and enrollments.
"""
import sys
from datetime import date
from app import create_app
from database import db
from repositories.user_repository import UserRepository
from repositories.student_repository import StudentRepository
from repositories.instructor_repository import InstructorRepository
from repositories.course_repository import CourseRepository
from repositories.semester_repository import SemesterRepository
from repositories.section_repository import SectionRepository
from repositories.enrollment_repository import EnrollmentRepository
from repositories.grade_repository import GradeRepository
from models import Course, Semester, ClassSection

def create_sample_data():
    app = create_app()
    with app.app_context():
        print("="*50)
        print("Creating Sample Data for edip_student")
        print("="*50)
        
        # Get edip_student user
        student_user = UserRepository.get_by_username('edip_student')
        if not student_user:
            print("[ERROR] edip_student user not found. Please login as student first.")
            return
        
        print(f"\n[OK] Found user: {student_user.username}")
        
        # Get or create student profile
        student = StudentRepository.get_by_user_id(student_user.user_id)
        if not student:
            student = StudentRepository.create(
                user_id=student_user.user_id,
                first_name='Edip',
                last_name='Student',
                email='edip@student.local'
            )
            print(f"[OK] Created student profile: {student.student_name}")
        else:
            print(f"[OK] Student profile exists: {student.student_name}")
        
        # Get or create instructor
        instructor_user = UserRepository.get_by_username('edip_instructor')
        if not instructor_user:
            instructor_user = UserRepository.create('edip_instructor', 'edip123', 'Instructor')
        
        instructor = InstructorRepository.get_by_user_id(instructor_user.user_id)
        if not instructor:
            instructor = InstructorRepository.create(
                user_id=instructor_user.user_id,
                first_name='Edip',
                last_name='Instructor',
                email='edip@instructor.local'
            )
            print(f"[OK] Created instructor: {instructor.full_name}")
        else:
            print(f"[OK] Instructor exists: {instructor.full_name}")
        
        # Assessment types are stored as strings in grades table
        # No need to create assessment_type records
        
        # Get or create course
        course = Course.query.filter_by(course_code='CS101').first()
        if not course:
            course = CourseRepository.create(
                course_name='Introduction to Computer Science',
                course_code='CS101',
                department='Computer Science',
                credits=3,
                description='An introductory course covering basic programming concepts'
            )
            print(f"[OK] Created course: {course.course_name}")
        else:
            print(f"[OK] Course exists: {course.course_name}")
        
        # Get or create semester
        semester = Semester.query.filter_by(semester_name='Fall', year=2024).first()
        if not semester:
            semester = SemesterRepository.create(
                term_name='Fall 2024',
                start_date=date(2024, 9, 1),
                end_date=date(2024, 12, 20)
            )
            print(f"[OK] Created semester: {semester.term_name}")
        else:
            print(f"[OK] Semester exists: {semester.term_name}")
        
        # Get or create section
        section = ClassSection.query.filter_by(
            course_id=course.course_id,
            semester_id=semester.semester_id,
            section_number='A'
        ).first()
        
        if not section:
            section = SectionRepository.create(
                course_id=course.course_id,
                instructor_id=instructor.instructor_id,
                semester_id=semester.semester_id,
                section_code='A',
                room='B-201',
                schedule_text='Mon 10:00-12:00'
            )
            print(f"[OK] Created section: {section.section_number}")
        else:
            print(f"[OK] Section exists: {section.section_number}")
        
        # Create enrollment if not exists
        from models import Enrollment
        enrollment = Enrollment.query.filter_by(
            student_id=student.student_id,
            section_id=section.section_id
        ).first()
        
        if not enrollment:
            enrollment = EnrollmentRepository.create(student.student_id, section.section_id)
            print(f"[OK] Created enrollment for {student.student_name}")
        else:
            print(f"[OK] Enrollment already exists for {student.student_name}")
        
        # Create sample grades if they don't exist
        from models import Grade
        midterm_grade = Grade.query.filter_by(
            enrollment_id=enrollment.enrollment_id,
            assessment_type='Midterm'
        ).first()
        
        if not midterm_grade:
            midterm_grade = Grade(
                enrollment_id=enrollment.enrollment_id,
                assessment_type='Midterm',
                score=85.00,
                max_score=100.00,
                weight=0.40  # 40% as decimal
            )
            db.session.add(midterm_grade)
            db.session.commit()
            print(f"[OK] Created Midterm grade: {midterm_grade.score}")
        else:
            print(f"[OK] Midterm grade already exists: {midterm_grade.score}")
        
        final_grade = Grade.query.filter_by(
            enrollment_id=enrollment.enrollment_id,
            assessment_type='Final'
        ).first()
        
        if not final_grade:
            final_grade = Grade(
                enrollment_id=enrollment.enrollment_id,
                assessment_type='Final',
                score=90.00,
                max_score=100.00,
                weight=0.60  # 60% as decimal
            )
            db.session.add(final_grade)
            db.session.commit()
            print(f"[OK] Created Final grade: {final_grade.score}")
        else:
            print(f"[OK] Final grade already exists: {final_grade.score}")
        
        print("\n" + "="*50)
        print("SUCCESS! Sample data created.")
        print("="*50)
        print(f"\nStudent: {student.student_name}")
        print(f"Course: {course.course_name} ({course.course_code})")
        print(f"Section: {section.section_number}")
        print(f"Semester: {semester.term_name}")
        print("="*50)

if __name__ == '__main__':
    try:
        create_sample_data()
    except Exception as e:
        print(f"\n[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


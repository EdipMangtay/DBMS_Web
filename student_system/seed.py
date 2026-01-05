"""
Seed script to populate the database with initial data.
Run this after setting up the database and .env file.
"""
import sys
from datetime import date, datetime
from app import create_app
from database import db
from models import User, Student, Instructor, Course, Semester, ClassSection, Enrollment, Grade, Department, AssessmentType
from repositories.user_repository import UserRepository
from repositories.department_repository import DepartmentRepository
from repositories.assessment_type_repository import AssessmentTypeRepository

def seed_database():
    app = create_app()
    with app.app_context():
        print("Starting database seeding...")
        
        # Create Departments
        print("Creating departments...")
        dept1 = DepartmentRepository.get_by_id(1)
        if not dept1:
            dept1 = DepartmentRepository.create('Computer Engineering')
            print(f"Department created: {dept1.department_name}")
        else:
            print(f"Department already exists: {dept1.department_name}")
        
        dept2 = DepartmentRepository.get_by_id(2)
        if not dept2:
            dept2 = DepartmentRepository.create('Software Engineering')
            print(f"Department created: {dept2.department_name}")
        else:
            print(f"Department already exists: {dept2.department_name}")
        
        # Create Assessment Types
        print("Creating assessment types...")
        midterm = AssessmentTypeRepository.get_by_name('Midterm')
        if not midterm:
            midterm = AssessmentTypeRepository.create('Midterm', 40.00)
            print(f"Assessment type created: {midterm.type_name}")
        else:
            print(f"Assessment type already exists: {midterm.type_name}")
        
        final = AssessmentTypeRepository.get_by_name('Final')
        if not final:
            final = AssessmentTypeRepository.create('Final', 60.00)
            print(f"Assessment type created: {final.type_name}")
        else:
            print(f"Assessment type already exists: {final.type_name}")
        
        # Create Admin user
        print("Creating admin user...")
        admin_user = UserRepository.get_by_username('admin')
        if not admin_user:
            admin_user = UserRepository.create('admin', 'admin123', 'Admin')
            print(f"Admin user created: {admin_user.username}")
        else:
            print(f"Admin user already exists: {admin_user.username}")
        
        # Create Instructor user (username = email for matching)
        print("Creating instructor user...")
        instructor_email = 'ali.yilmaz@isu.edu'
        instructor_user = UserRepository.get_by_username(instructor_email)
        if not instructor_user:
            instructor_user = UserRepository.create(instructor_email, 'instructor123', 'Instructor', email=instructor_email)
            print(f"Instructor user created: {instructor_user.username}")
        else:
            print(f"Instructor user already exists: {instructor_user.username}")
        
        instructor = Instructor.query.filter_by(email=instructor_email).first()
        if not instructor:
            instructor = Instructor(
                full_name='Dr. Ali Yilmaz',
                email=instructor_email
            )
            db.session.add(instructor)
            db.session.commit()
            print(f"Instructor created: {instructor.full_name}")
        else:
            print(f"Instructor already exists: {instructor.full_name}")
        
        # Create Student user (username = email for matching)
        print("Creating student user...")
        student_email = 'sojod.ahmed@isu.edu'
        student_user = UserRepository.get_by_username(student_email)
        if not student_user:
            student_user = UserRepository.create(student_email, 'student123', 'Student', email=student_email)
            print(f"Student user created: {student_user.username}")
        else:
            print(f"Student user already exists: {student_user.username}")
        
        student = Student.query.filter_by(student_mail=student_email).first()
        if not student:
            student = Student(
                student_name='Sojod Ahmed',
                student_mail=student_email
            )
            db.session.add(student)
            db.session.commit()
            print(f"Student created: {student.student_name}")
        else:
            print(f"Student already exists: {student.student_name}")
        
        # Create Course
        print("Creating course...")
        course = Course.query.filter_by(course_name='Database Systems').first()
        if not course:
            course = Course(
                course_name='Database Systems',
                department_id=dept2.department_id,
                instructor_id=instructor.instructor_id
            )
            db.session.add(course)
            db.session.commit()
            print(f"Course created: {course.course_name}")
        else:
            print(f"Course already exists: {course.course_name}")
        
        # Create Semester
        print("Creating semester...")
        semester = Semester.query.filter_by(term_name='Fall 2025').first()
        if not semester:
            semester = Semester(
                term_name='Fall 2025',
                start_date=date(2025, 9, 15),
                end_date=date(2026, 1, 10)
            )
            db.session.add(semester)
            db.session.commit()
            print(f"Semester created: {semester.term_name}")
        else:
            print(f"Semester already exists: {semester.term_name}")
        
        # Create Section
        print("Creating section...")
        from repositories.section_repository import SectionRepository
        section = SectionRepository.get_by_id(1)
        if not section:
            section = SectionRepository.create(
                course_id=course.course_id,
                instructor_id=instructor.instructor_id,
                semester_id=semester.semester_id,
                section_code='A',
                room='B-201',
                schedule_text='Mon 10:00-12:00'
            )
            print(f"Section created: {section.section_code}")
        else:
            print(f"Section already exists: {section.section_code}")
        
        # Create Enrollment
        print("Creating enrollment...")
        from repositories.enrollment_repository import EnrollmentRepository
        from models import Enrollment
        enrollment_exists = EnrollmentRepository.exists(student.student_id, section.section_id)
        if not enrollment_exists:
            enrollment = EnrollmentRepository.create(student.student_id, section.section_id)
            print(f"Enrollment created for {student.student_name}")
        else:
            enrollment = Enrollment.query.filter_by(
                student_id=student.student_id,
                section_id=section.section_id
            ).first()
            print(f"Enrollment already exists for {student.student_name}")
        
        # Create Sample Grades
        print("Creating sample grades...")
        from repositories.grade_repository import GradeRepository
        midterm_grade = GradeRepository.get_by_assessment_type(enrollment.enrollment_id, midterm.assessment_type_id)
        if not midterm_grade:
            midterm_grade = GradeRepository.create(enrollment.enrollment_id, midterm.assessment_type_id, 92.50)
            print(f"Midterm grade created: {midterm_grade.score}")
        else:
            print(f"Midterm grade already exists: {midterm_grade.score}")
        
        final_grade = GradeRepository.get_by_assessment_type(enrollment.enrollment_id, final.assessment_type_id)
        if not final_grade:
            final_grade = GradeRepository.create(enrollment.enrollment_id, final.assessment_type_id, 88.00)
            print(f"Final grade created: {final_grade.score}")
        else:
            print(f"Final grade already exists: {final_grade.score}")
        
        print("\n" + "="*50)
        print("Database seeding completed successfully!")
        print("="*50)
        print("\nDefault credentials:")
        print("Admin:     username=admin, password=admin123")
        print("Instructor: username=ali.yilmaz@isu.edu, password=instructor123")
        print("Student:   username=sojod.ahmed@isu.edu, password=student123")
        print("\nPlease change these passwords after first login!")

if __name__ == '__main__':
    try:
        seed_database()
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

from database import db
from models import Enrollment, Student, ClassSection, Course, Semester
from sqlalchemy import func
from datetime import date

class EnrollmentRepository:
    @staticmethod
    def get_by_id(enrollment_id):
        return Enrollment.query.get(enrollment_id)
    
    @staticmethod
    def get_by_student(student_id, page=1, per_page=20):
        # Get enrollments with all relationships loaded (except grades - it's dynamic)
        from sqlalchemy.orm import joinedload
        return Enrollment.query.filter_by(student_id=student_id)\
            .options(
                joinedload(Enrollment.section).joinedload(ClassSection.course),
                joinedload(Enrollment.section).joinedload(ClassSection.semester),
                joinedload(Enrollment.section).joinedload(ClassSection.instructor)
            )\
            .paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_all_by_student(student_id):
        """Get all enrollments for a student without pagination (for statistics)"""
        return Enrollment.query.filter_by(student_id=student_id).join(ClassSection).join(Course).join(Semester).all()
    
    @staticmethod
    def get_by_section(section_id, page=1, per_page=50):
        return Enrollment.query.filter_by(section_id=section_id).join(Student).paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_all_by_section(section_id):
        """Get all enrollments for a section without pagination (for statistics)"""
        return Enrollment.query.filter_by(section_id=section_id).join(Student).all()
    
    @staticmethod
    def create(student_id, section_id, enroll_date=None):
        if enroll_date is None:
            enroll_date = date.today()
        enrollment = Enrollment(
            student_id=student_id,
            section_id=section_id,
            enrollment_date=enroll_date  # SQL'de enrollment_date
        )
        db.session.add(enrollment)
        db.session.commit()
        return enrollment
    
    @staticmethod
    def update(enrollment_id, **kwargs):
        enrollment = Enrollment.query.get(enrollment_id)
        if enrollment:
            for key, value in kwargs.items():
                if hasattr(enrollment, key) and value is not None:
                    setattr(enrollment, key, value)
            db.session.commit()
        return enrollment
    
    @staticmethod
    def delete(enrollment_id):
        enrollment = Enrollment.query.get(enrollment_id)
        if enrollment:
            db.session.delete(enrollment)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def exists(student_id, section_id):
        return Enrollment.query.filter_by(student_id=student_id, section_id=section_id).first() is not None

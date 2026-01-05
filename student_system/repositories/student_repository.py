from database import db
from models import Student
from sqlalchemy import func

class StudentRepository:
    @staticmethod
    def get_by_id(student_id):
        return Student.query.get(student_id)
    
    @staticmethod
    def get_by_email(email):
        return Student.query.filter_by(student_mail=email).first()
    
    @staticmethod
    def get_by_user_email(email):
        """Get student by user email (for authentication)"""
        return Student.query.filter_by(student_mail=email).first()
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get student by user_id (for authentication)"""
        return Student.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def get_all(page=1, per_page=20):
        return Student.query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def create(user_id, first_name, last_name, email, phone=None, date_of_birth=None, enrollment_date=None):
        student = Student(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            enrollment_date=enrollment_date
        )
        db.session.add(student)
        db.session.commit()
        return student
    
    @staticmethod
    def update(student_id, **kwargs):
        student = Student.query.get(student_id)
        if student:
            for key, value in kwargs.items():
                if hasattr(student, key) and value is not None:
                    setattr(student, key, value)
            db.session.commit()
        return student
    
    @staticmethod
    def delete(student_id):
        student = Student.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def search(query, page=1, per_page=20):
        search_filter = db.or_(
            Student.student_name.ilike(f'%{query}%'),
            Student.student_mail.ilike(f'%{query}%')
        )
        return Student.query.filter(search_filter).paginate(page=page, per_page=per_page, error_out=False)

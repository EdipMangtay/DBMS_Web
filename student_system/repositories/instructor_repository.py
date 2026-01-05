from database import db
from models import Instructor

class InstructorRepository:
    @staticmethod
    def get_by_id(instructor_id):
        return Instructor.query.get(instructor_id)
    
    @staticmethod
    def get_by_email(email):
        return Instructor.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_user_email(email):
        """Get instructor by user email (for authentication)"""
        return Instructor.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get instructor by user_id (for authentication)"""
        return Instructor.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def get_all(page=1, per_page=20):
        return Instructor.query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def create(user_id, first_name, last_name, email, phone=None, department=None, hire_date=None):
        instructor = Instructor(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            department=department,
            hire_date=hire_date
        )
        db.session.add(instructor)
        db.session.commit()
        return instructor
    
    @staticmethod
    def update(instructor_id, **kwargs):
        instructor = Instructor.query.get(instructor_id)
        if instructor:
            for key, value in kwargs.items():
                if hasattr(instructor, key) and value is not None:
                    setattr(instructor, key, value)
            db.session.commit()
        return instructor
    
    @staticmethod
    def delete(instructor_id):
        instructor = Instructor.query.get(instructor_id)
        if instructor:
            db.session.delete(instructor)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def search(query, page=1, per_page=20):
        search_filter = db.or_(
            Instructor.full_name.ilike(f'%{query}%'),
            Instructor.email.ilike(f'%{query}%')
        )
        return Instructor.query.filter(search_filter).paginate(page=page, per_page=per_page, error_out=False)

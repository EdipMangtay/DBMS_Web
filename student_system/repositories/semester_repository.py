from database import db
from models import Semester

class SemesterRepository:
    @staticmethod
    def get_by_id(semester_id):
        return Semester.query.get(semester_id)
    
    @staticmethod
    def get_all():
        return Semester.query.order_by(Semester.start_date.desc()).all()
    
    @staticmethod
    def create(term_name, start_date, end_date):
        # Parse term_name to extract semester_name and year
        # e.g., "Fall 2025" -> semester_name="Fall", year=2025
        parts = term_name.split(' ')
        semester_name = parts[0] if parts else term_name
        year = None
        if len(parts) > 1:
            try:
                year = int(parts[-1])
            except:
                # If year not found, try to extract from start_date
                if start_date:
                    year = start_date.year
        
        if year is None:
            year = start_date.year if start_date else 2024
        
        semester = Semester(
            semester_name=semester_name,
            year=year,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(semester)
        db.session.commit()
        return semester
    
    @staticmethod
    def update(semester_id, **kwargs):
        semester = Semester.query.get(semester_id)
        if semester:
            for key, value in kwargs.items():
                if hasattr(semester, key) and value is not None:
                    setattr(semester, key, value)
            db.session.commit()
        return semester

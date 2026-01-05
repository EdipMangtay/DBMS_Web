from database import db
from models import Course

class CourseRepository:
    @staticmethod
    def get_by_id(course_id):
        return Course.query.get(course_id)
    
    @staticmethod
    def get_all(page=1, per_page=20):
        return Course.query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_by_instructor(instructor_id, page=1, per_page=20):
        # Courses don't have instructor_id, sections do
        # Get courses through sections
        from models import ClassSection
        section_ids = ClassSection.query.filter_by(instructor_id=instructor_id).with_entities(ClassSection.course_id).distinct().all()
        course_ids = [s[0] for s in section_ids]
        if not course_ids:
            # Return empty pagination
            from flask_sqlalchemy import Pagination
            return Pagination(query=None, page=page, per_page=per_page, total=0, items=[])
        return Course.query.filter(Course.course_id.in_(course_ids)).paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def create(course_name, course_code, department=None, credits=3, description=None):
        course = Course(
            course_code=course_code,
            course_name=course_name,
            department=department,  # String, not foreign key
            credits=credits,
            description=description
        )
        db.session.add(course)
        db.session.commit()
        return course
    
    @staticmethod
    def update(course_id, **kwargs):
        course = Course.query.get(course_id)
        if course:
            for key, value in kwargs.items():
                if hasattr(course, key) and value is not None:
                    setattr(course, key, value)
            db.session.commit()
        return course
    
    @staticmethod
    def delete(course_id):
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def search(query, page=1, per_page=20):
        search_filter = db.or_(
            Course.course_name.ilike(f'%{query}%')
        )
        return Course.query.filter(search_filter).paginate(page=page, per_page=per_page, error_out=False)

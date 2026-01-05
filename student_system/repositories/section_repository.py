from database import db
from models import ClassSection, Course, Instructor, Semester

class SectionRepository:
    @staticmethod
    def get_by_id(section_id):
        return ClassSection.query.get(section_id)
    
    @staticmethod
    def get_all(page=1, per_page=20):
        return ClassSection.query.join(Course).join(Semester).paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_by_instructor(instructor_id, page=1, per_page=20):
        return ClassSection.query.filter_by(instructor_id=instructor_id).join(Course).join(Semester).paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_by_course(course_id, page=1, per_page=20):
        return ClassSection.query.filter_by(course_id=course_id).join(Semester).paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def create(course_id, instructor_id, semester_id, section_code, room=None, schedule_text=None):
        # SQL'de section_number kullanılıyor, section_code property olarak dönüyor
        section = ClassSection(
            course_id=course_id,
            instructor_id=instructor_id,
            semester_id=semester_id,
            section_number=section_code,  # SQL'de section_number
            room=room,
            schedule=schedule_text  # SQL'de schedule
        )
        db.session.add(section)
        db.session.commit()
        return section
    
    @staticmethod
    def update(section_id, **kwargs):
        section = ClassSection.query.get(section_id)
        if section:
            for key, value in kwargs.items():
                if hasattr(section, key) and value is not None:
                    setattr(section, key, value)
            db.session.commit()
        return section
    
    @staticmethod
    def delete(section_id):
        section = ClassSection.query.get(section_id)
        if section:
            db.session.delete(section)
            db.session.commit()
            return True
        return False

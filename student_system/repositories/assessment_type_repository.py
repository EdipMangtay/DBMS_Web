from database import db
from models import AssessmentType

class AssessmentTypeRepository:
    @staticmethod
    def get_by_id(assessment_type_id):
        return AssessmentType.query.get(assessment_type_id)
    
    @staticmethod
    def get_all():
        return AssessmentType.query.all()
    
    @staticmethod
    def get_by_name(type_name):
        return AssessmentType.query.filter_by(type_name=type_name).first()
    
    @staticmethod
    def create(type_name, weight):
        assessment_type = AssessmentType(
            type_name=type_name,
            weight=weight
        )
        db.session.add(assessment_type)
        db.session.commit()
        return assessment_type
    
    @staticmethod
    def update(assessment_type_id, **kwargs):
        assessment_type = AssessmentType.query.get(assessment_type_id)
        if assessment_type:
            for key, value in kwargs.items():
                if hasattr(assessment_type, key) and value is not None:
                    setattr(assessment_type, key, value)
            db.session.commit()
        return assessment_type
    
    @staticmethod
    def delete(assessment_type_id):
        assessment_type = AssessmentType.query.get(assessment_type_id)
        if assessment_type:
            db.session.delete(assessment_type)
            db.session.commit()
            return True
        return False





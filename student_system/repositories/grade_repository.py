from database import db
from models import Grade, Enrollment, AssessmentType
from sqlalchemy import func

class GradeRepository:
    @staticmethod
    def get_by_id(grade_id):
        return Grade.query.get(grade_id)
    
    @staticmethod
    def get_by_enrollment(enrollment_id):
        return Grade.query.filter_by(enrollment_id=enrollment_id).all()
    
    @staticmethod
    def create(enrollment_id, assessment_type_id, score):
        # Get assessment type name from ID
        assessment_type = AssessmentType.query.get(assessment_type_id)
        if not assessment_type:
            raise ValueError(f"AssessmentType with id {assessment_type_id} not found")
        
        grade = Grade(
            enrollment_id=enrollment_id,
            assessment_type=assessment_type.type_name,  # SQL'de string
            score=score,
            weight=assessment_type.weight,
            max_score=100.00
        )
        db.session.add(grade)
        db.session.commit()
        return grade
    
    @staticmethod
    def update(grade_id, **kwargs):
        grade = Grade.query.get(grade_id)
        if grade:
            for key, value in kwargs.items():
                if hasattr(grade, key) and value is not None:
                    setattr(grade, key, value)
            db.session.commit()
        return grade
    
    @staticmethod
    def delete(grade_id):
        grade = Grade.query.get(grade_id)
        if grade:
            db.session.delete(grade)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_by_assessment_type(enrollment_id, assessment_type_id):
        # Get assessment type name from ID
        assessment_type = AssessmentType.query.get(assessment_type_id)
        if not assessment_type:
            return None
        return Grade.query.filter_by(enrollment_id=enrollment_id, assessment_type=assessment_type.type_name).first()
    
    @staticmethod
    def calculate_enrollment_average(enrollment_id):
        """Calculate weighted average for an enrollment using Grade weights"""
        grades = Grade.query.filter_by(enrollment_id=enrollment_id).all()
        if not grades:
            return None
        
        total_weighted_score = 0
        total_weight = 0
        
        for grade in grades:
            score = float(grade.score)
            # Use weight from grade (SQL'de weight kolonu var)
            weight = float(grade.weight) if grade.weight else 1.0
            total_weighted_score += score * weight
            total_weight += weight
        
        if total_weight == 0:
            return None
        
        return total_weighted_score / total_weight

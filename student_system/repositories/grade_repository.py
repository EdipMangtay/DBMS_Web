from database import db
from models import Grade, Enrollment
from sqlalchemy import func
from datetime import date

class GradeRepository:
    @staticmethod
    def get_by_id(grade_id):
        return Grade.query.get(grade_id)
    
    @staticmethod
    def get_by_enrollment(enrollment_id):
        return Grade.query.filter_by(enrollment_id=enrollment_id).all()
    
    @staticmethod
    def create(enrollment_id, assessment_type_id, score):
        # Legacy method - kept for backward compatibility
        # assessment_type_id is actually assessment_type string now
        return GradeRepository.create_grade(
            enrollment_id=enrollment_id,
            assessment_type=str(assessment_type_id),
            score=score,
            max_score=100.00,
            weight=None
        )
    
    @staticmethod
    def create_grade(enrollment_id, assessment_type, score, max_score=100.00, weight=None, notes=None):
        """Create a grade with string-based assessment_type"""
        grade = Grade(
            enrollment_id=enrollment_id,
            assessment_type=assessment_type,  # String, not foreign key
            score=score,
            max_score=max_score,
            weight=weight,  # Decimal between 0 and 1
            notes=notes,
            graded_date=date.today()
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
        # Legacy method - kept for backward compatibility
        # assessment_type_id is actually assessment_type string now
        return GradeRepository.get_by_assessment_type_name(enrollment_id, str(assessment_type_id))
    
    @staticmethod
    def get_by_assessment_type_name(enrollment_id, assessment_type):
        """Get grade by enrollment_id and assessment_type (string)"""
        return Grade.query.filter_by(enrollment_id=enrollment_id, assessment_type=assessment_type).first()
    
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

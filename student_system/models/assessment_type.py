from database import db

class AssessmentType(db.Model):
    __tablename__ = 'assessment_types'
    
    assessment_type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)
    weight = db.Column(db.Numeric(5, 2), nullable=False)
    
    # Note: Grades table uses assessment_type as string, not foreign key
    # No direct relationship defined
    
    def __repr__(self):
        return f'<AssessmentType {self.type_name}>'





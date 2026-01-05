from database import db

class Grade(db.Model):
    __tablename__ = 'grades'
    
    grade_id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'), nullable=False)
    assessment_type = db.Column(db.String(50), nullable=False)  # SQL'de string, not foreign key
    score = db.Column(db.Numeric(5, 2), nullable=False)
    max_score = db.Column(db.Numeric(5, 2), default=100.00, nullable=True)
    weight = db.Column(db.Numeric(5, 2), nullable=True)
    graded_date = db.Column(db.Date, server_default=db.func.current_date(), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Properties for compatibility with AssessmentType
    @property
    def assessment_type_id(self):
        # Try to find AssessmentType by name
        try:
            from models import AssessmentType
            at = AssessmentType.query.filter_by(type_name=self.assessment_type).first()
            return at.assessment_type_id if at else None
        except:
            return None
    
    @property
    def assessment_type_obj(self):
        try:
            from models import AssessmentType
            return AssessmentType.query.filter_by(type_name=self.assessment_type).first()
        except:
            return None
    
    def __repr__(self):
        return f'<Grade {self.score}>'

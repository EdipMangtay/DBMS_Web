from database import db

class Section(db.Model):
    __tablename__ = 'sections'
    
    section_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id', ondelete='SET NULL'), nullable=True)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.semester_id', ondelete='CASCADE'), nullable=False)
    section_number = db.Column(db.String(10), nullable=False)
    capacity = db.Column(db.Integer, default=30)
    schedule = db.Column(db.String(100))  # e.g., "MWF 10:00-11:00"
    room = db.Column(db.String(50))
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='section', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Section {self.section_number}>'


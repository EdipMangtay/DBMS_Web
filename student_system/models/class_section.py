from database import db

class ClassSection(db.Model):
    __tablename__ = 'sections'
    
    section_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.semester_id', ondelete='RESTRICT'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id', ondelete='SET NULL'), nullable=True)
    section_number = db.Column(db.String(10), nullable=False)  # SQL'de section_number
    capacity = db.Column(db.Integer, nullable=True)
    schedule = db.Column(db.String(100), nullable=True)  # SQL'de schedule
    room = db.Column(db.String(50), nullable=True)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='section', lazy='dynamic', cascade='all, delete-orphan')
    
    # Properties for compatibility
    @property
    def section_code(self):
        return self.section_number
    
    @property
    def schedule_text(self):
        return self.schedule
    
    def __repr__(self):
        return f'<ClassSection {self.section_code}>'





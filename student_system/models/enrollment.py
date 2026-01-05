from database import db

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.section_id', ondelete='CASCADE'), nullable=False)
    enrollment_date = db.Column(db.Date, server_default=db.func.current_date(), nullable=False)
    status = db.Column(db.String(20), default='Active', nullable=True)
    
    # Relationships
    grades = db.relationship('Grade', backref='enrollment', lazy='dynamic', cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', backref='enrollment', lazy='dynamic', cascade='all, delete-orphan')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('student_id', 'section_id', name='unique_student_section'),)
    
    # Properties for compatibility
    @property
    def enroll_date(self):
        return self.enrollment_date
    
    def __repr__(self):
        return f'<Enrollment {self.enrollment_id}>'

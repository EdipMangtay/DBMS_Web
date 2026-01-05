from database import db

class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    enrollment_date = db.Column(db.Date, nullable=True)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    
    # Properties for compatibility
    @property
    def student_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def student_mail(self):
        return self.email
    
    @property
    def full_name(self):
        return self.student_name
    
    def __repr__(self):
        return f'<Student {self.student_name}>'

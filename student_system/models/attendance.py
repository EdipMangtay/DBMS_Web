from database import db

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    attendance_id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.enrollment_id', ondelete='CASCADE'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Present', 'Absent', 'Excused'), nullable=False, default='Present')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('enrollment_id', 'attendance_date', name='unique_enrollment_date'),)
    
    def __repr__(self):
        return f'<Attendance {self.status} on {self.attendance_date}>'





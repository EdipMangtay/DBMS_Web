from database import db

class Course(db.Model):
    __tablename__ = 'courses'
    
    course_id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    credits = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=True)  # String, not foreign key in SQL
    
    # Relationships
    sections = db.relationship('ClassSection', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.course_name}>'

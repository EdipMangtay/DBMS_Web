from database import db

class Instructor(db.Model):
    __tablename__ = 'instructors'
    
    instructor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    hire_date = db.Column(db.Date, nullable=True)
    
    # Relationships
    sections = db.relationship('ClassSection', backref='instructor', lazy='dynamic')
    
    # Properties for compatibility
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def __repr__(self):
        return f'<Instructor {self.full_name}>'

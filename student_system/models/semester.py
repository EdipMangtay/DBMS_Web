from database import db

class Semester(db.Model):
    __tablename__ = 'semesters'
    
    semester_id = db.Column(db.Integer, primary_key=True)
    semester_name = db.Column(db.String(50), nullable=False)  # SQL'de semester_name
    year = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, nullable=True)
    
    # Relationships
    sections = db.relationship('ClassSection', backref='semester', lazy='dynamic')
    
    # Properties for compatibility
    @property
    def term_name(self):
        return f"{self.semester_name} {self.year}"
    
    @property
    def display_name(self):
        return self.term_name
    
    def __repr__(self):
        return f'<Semester {self.term_name}>'

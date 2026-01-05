from database import db

class Department(db.Model):
    __tablename__ = 'departments'
    
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Note: In SQL, courses.department is a string, not a foreign key
    # So we cannot define a relationship here
    # Use Course.query.filter_by(department=department_name) instead
    
    def __repr__(self):
        return f'<Department {self.department_name}>'





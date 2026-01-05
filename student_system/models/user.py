from flask_login import UserMixin
from database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)  # Admin, Instructor, Student
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def get_id(self):
        return str(self.user_id)
    
    @property
    def email(self):
        """Return username as email for compatibility"""
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'

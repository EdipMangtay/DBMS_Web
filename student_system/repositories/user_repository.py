from database import db
from models import User
from werkzeug.security import check_password_hash, generate_password_hash

class UserRepository:
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_email(email):
        # Username is used as email
        return User.query.filter_by(username=email).first()
    
    @staticmethod
    def create(username, password, role, email=None):
        # If email is provided, use it as username, otherwise use username
        actual_username = email if email else username
        user = User(
            username=actual_username,
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user.password_hash, password)
    
    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def get_by_role(role):
        return User.query.filter_by(role=role).all()

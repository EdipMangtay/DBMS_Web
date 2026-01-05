from database import db
from models import Department

class DepartmentRepository:
    @staticmethod
    def get_by_id(department_id):
        return Department.query.get(department_id)
    
    @staticmethod
    def get_all():
        return Department.query.all()
    
    @staticmethod
    def create(department_name):
        department = Department(department_name=department_name)
        db.session.add(department)
        db.session.commit()
        return department
    
    @staticmethod
    def update(department_id, department_name):
        department = Department.query.get(department_id)
        if department:
            department.department_name = department_name
            db.session.commit()
        return department
    
    @staticmethod
    def delete(department_id):
        department = Department.query.get(department_id)
        if department:
            db.session.delete(department)
            db.session.commit()
            return True
        return False





"""
Script to create or update admin and student users with simple credentials.
Run this to ensure users exist in the database.
"""
import sys
from app import create_app
from database import db
from repositories.user_repository import UserRepository
from repositories.student_repository import StudentRepository
from werkzeug.security import generate_password_hash

def create_or_update_users():
    app = create_app()
    with app.app_context():
        print("="*50)
        print("Creating/Updating Users")
        print("="*50)
        
        # Create/Update Admin user
        print("\n1. Admin User:")
        admin_user = UserRepository.get_by_username('admin')
        if admin_user:
            # Update password
            admin_user.password_hash = generate_password_hash('admin123')
            db.session.commit()
            print(f"   [OK] Admin user exists - password updated")
            print(f"   Username: admin")
            print(f"   Password: admin123")
        else:
            admin_user = UserRepository.create('admin', 'admin123', 'Admin')
            print(f"   [OK] Admin user created")
            print(f"   Username: admin")
            print(f"   Password: admin123")
        
        # Create/Update Student user
        print("\n2. Student User:")
        student_user = UserRepository.get_by_username('student')
        if student_user:
            # Update password
            student_user.password_hash = generate_password_hash('student123')
            db.session.commit()
            print(f"   [OK] Student user exists - password updated")
            print(f"   Username: student")
            print(f"   Password: student123")
        else:
            student_user = UserRepository.create('student', 'student123', 'Student')
            print(f"   [OK] Student user created")
            print(f"   Username: student")
            print(f"   Password: student123")
        
        # Create/Update Student profile
        print("\n3. Student Profile:")
        student_profile = StudentRepository.get_by_user_id(student_user.user_id)
        if not student_profile:
            student_email = 'student@student.local'
            # Check if email already exists
            existing = StudentRepository.get_by_email(student_email)
            if existing:
                # Update existing student to link with user
                existing.user_id = student_user.user_id
                db.session.commit()
                student_profile = existing
                print(f"   [OK] Student profile linked to user")
            else:
                student_profile = StudentRepository.create(
                    user_id=student_user.user_id,
                    first_name='Student',
                    last_name='User',
                    email=student_email
                )
                print(f"   [OK] Student profile created")
        else:
            print(f"   [OK] Student profile already exists")
        
        print("\n" + "="*50)
        print("SUCCESS! Users are ready to use.")
        print("="*50)
        print("\nLogin Credentials:")
        print("Admin:   username=admin,   password=admin123")
        print("Student: username=student,  password=student123")
        print("\nLogin URLs:")
        print("Admin:   /auth/admin/login")
        print("Student: /auth/student/login")
        print("="*50)

if __name__ == '__main__':
    try:
        create_or_update_users()
    except Exception as e:
        print(f"\n[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


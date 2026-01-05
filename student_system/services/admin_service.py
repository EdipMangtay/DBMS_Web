from repositories import (
    StudentRepository, InstructorRepository, CourseRepository,
    SemesterRepository, SectionRepository, EnrollmentRepository,
    DepartmentRepository, UserRepository
)

class AdminService:
    @staticmethod
    def create_student(username, password, student_name, student_mail):
        # Create user first - use student_mail as username for email matching
        user = UserRepository.create(username, password, 'Student', email=student_mail)
        
        # Split student_name into first_name and last_name
        name_parts = student_name.split(' ', 1)
        first_name = name_parts[0] if name_parts else student_name
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create student profile
        student = StudentRepository.create(
            user_id=user.user_id,
            first_name=first_name,
            last_name=last_name,
            email=student_mail
        )
        return student
    
    @staticmethod
    def create_instructor(username, password, full_name, email):
        # Create user first - use email as username for email matching
        user = UserRepository.create(username, password, 'Instructor', email=email)
        
        # Split full_name into first_name and last_name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0] if name_parts else full_name
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create instructor profile
        instructor = InstructorRepository.create(
            user_id=user.user_id,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        return instructor
    
    @staticmethod
    def create_course(course_name, course_code, department=None, credits=3, description=None):
        return CourseRepository.create(course_name, course_code, department, credits, description)
    
    @staticmethod
    def get_students(page=1, per_page=20, search=None):
        if search:
            return StudentRepository.search(search, page, per_page)
        return StudentRepository.get_all(page, per_page)
    
    @staticmethod
    def get_instructors(page=1, per_page=20, search=None):
        if search:
            return InstructorRepository.search(search, page, per_page)
        return InstructorRepository.get_all(page, per_page)
    
    @staticmethod
    def get_courses(page=1, per_page=20, search=None):
        if search:
            return CourseRepository.search(search, page, per_page)
        return CourseRepository.get_all(page, per_page)
    
    @staticmethod
    def get_departments():
        # Departments table doesn't exist in SQL, return empty list
        # Department is just a string field in courses table
        return []
    
    @staticmethod
    def update_student(student_id, **kwargs):
        return StudentRepository.update(student_id, **kwargs)
    
    @staticmethod
    def update_instructor(instructor_id, **kwargs):
        return InstructorRepository.update(instructor_id, **kwargs)
    
    @staticmethod
    def update_course(course_id, course_name=None, course_code=None, department=None, credits=None, description=None):
        kwargs = {}
        if course_name:
            kwargs['course_name'] = course_name
        if course_code:
            kwargs['course_code'] = course_code
        if department is not None:
            kwargs['department'] = department
        if credits:
            kwargs['credits'] = credits
        if description is not None:
            kwargs['description'] = description
        
        return CourseRepository.update(course_id, **kwargs)
    
    @staticmethod
    def delete_student(student_id):
        return StudentRepository.delete(student_id)
    
    @staticmethod
    def delete_instructor(instructor_id):
        return InstructorRepository.delete(instructor_id)
    
    @staticmethod
    def delete_course(course_id):
        return CourseRepository.delete(course_id)
    
    @staticmethod
    def create_semester(term_name, start_date, end_date):
        return SemesterRepository.create(term_name, start_date, end_date)
    
    @staticmethod
    def create_section(course_id, instructor_id, semester_id, section_code, room=None, schedule_text=None):
        return SectionRepository.create(course_id, instructor_id, semester_id, section_code, room, schedule_text)
    
    @staticmethod
    def enroll_student(student_id, section_id):
        if EnrollmentRepository.exists(student_id, section_id):
            return None, "Student is already enrolled in this section"
        enrollment = EnrollmentRepository.create(student_id, section_id)
        return enrollment, None

from repositories import EnrollmentRepository, GradeRepository, StudentRepository
from database import db

class StudentService:
    @staticmethod
    def get_student_enrollments(student_id, page=1, per_page=20):
        return EnrollmentRepository.get_by_student(student_id, page, per_page)
    
    @staticmethod
    def get_transcript_details(student_id):
        """Get transcript details - try view first, fallback to query"""
        try:
            # Try to query view if it exists
            result = db.session.execute(
                db.text('SELECT * FROM View_StudentTranscriptDetails WHERE student_id = :student_id'),
                {'student_id': student_id}
            )
            rows = result.fetchall()
            if rows:
                return [dict(row._mapping) for row in rows]
        except Exception:
            pass
        
        # Fallback: compute with SQLAlchemy
        from models import Enrollment, ClassSection, Course, Semester, Grade
        
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        transcript = []
        
        for enrollment in enrollments:
            section = enrollment.section
            course = section.course
            semester = section.semester
            
            # Calculate student average
            avg = GradeRepository.calculate_enrollment_average(enrollment.enrollment_id)
            
            # Calculate class average (all students in this section)
            section_enrollments = Enrollment.query.filter_by(section_id=section.section_id).all()
            section_averages = []
            for sec_enr in section_enrollments:
                sec_avg = GradeRepository.calculate_enrollment_average(sec_enr.enrollment_id)
                if sec_avg is not None:
                    section_averages.append(sec_avg)
            
            class_avg = sum(section_averages) / len(section_averages) if section_averages else None
            
            # Calculate letter grade
            letter_grade = StudentService.calculate_letter_grade(avg) if avg else None
            
            transcript.append({
                'course_code': course.course_code,
                'course_name': course.course_name,
                'credits': course.credits,
                'semester': semester.term_name,
                'student_average': float(avg) if avg else None,
                'class_average': float(class_avg) if class_avg else None,
                'letter_grade': letter_grade
            })
        
        return transcript
    
    @staticmethod
    def calculate_letter_grade(score):
        """Calculate letter grade - try function first, fallback to logic"""
        if score is None:
            return None
        
        try:
            # Try to call function if it exists
            result = db.session.execute(
                db.text('SELECT CalculateLetterGrade(:score)'),
                {'score': score}
            )
            letter = result.scalar()
            if letter:
                return letter
        except Exception:
            pass
        
        # Fallback: standard grading scale (matching database function)
        if score >= 90:
            return 'AA'
        elif score >= 85:
            return 'BA'
        elif score >= 80:
            return 'BB'
        elif score >= 75:
            return 'CB'
        elif score >= 70:
            return 'CC'
        elif score >= 65:
            return 'DC'
        elif score >= 60:
            return 'DD'
        elif score >= 50:
            return 'FD'
        else:
            return 'FF'
    
    @staticmethod
    def get_overall_average(student_id):
        """Get overall average - try view first, fallback to computation"""
        try:
            # Try to query view if it exists
            result = db.session.execute(
                db.text('SELECT average_score FROM StudentAverage WHERE student_id = :student_id'),
                {'student_id': student_id}
            )
            avg = result.scalar()
            if avg is not None:
                return float(avg)
        except Exception:
            pass
        
        # Compute from all enrollments
        enrollments = EnrollmentRepository.get_all_by_student(student_id)
        averages = []
        
        for enrollment in enrollments:
            avg = GradeRepository.calculate_enrollment_average(enrollment.enrollment_id)
            if avg is not None:
                averages.append(avg)
        
        if not averages:
            return None
        
        return sum(averages) / len(averages)

from database import db

class ReportService:
    @staticmethod
    def get_course_performance_report():
        """Get course performance report - try view first, fallback to query"""
        try:
            # Try to query view if it exists
            result = db.session.execute(
                db.text('SELECT * FROM View_CoursePerformanceReport')
            )
            rows = result.fetchall()
            if rows:
                return [dict(row._mapping) for row in rows]
        except Exception:
            pass
        
        # Fallback: compute with SQLAlchemy
        from models import Course, ClassSection, Enrollment, Grade
        from repositories.grade_repository import GradeRepository
        
        courses = Course.query.all()
        report = []
        
        for course in courses:
            # Get sections for this course
            sections = ClassSection.query.filter_by(course_id=course.course_id).all()
            section_ids = [s.section_id for s in sections]
            
            if not section_ids:
                report.append({
                    'course_code': course.course_code,
                    'course_name': course.course_name,
                    'total_students': 0,
                    'average_grade': None,
                    'pass_rate': None
                })
                continue
            
            # Get all enrollments for this course
            enrollments = Enrollment.query.filter(Enrollment.section_id.in_(section_ids)).all()
            enrollment_ids = [e.enrollment_id for e in enrollments]
            
            if not enrollment_ids:
                report.append({
                    'course_code': course.course_code,
                    'course_name': course.course_name,
                    'total_students': 0,
                    'average_grade': None,
                    'pass_rate': None
                })
                continue
            
            # Calculate averages and pass rate
            averages = []
            passed_count = 0
            student_ids = set()
            
            for enrollment_id in enrollment_ids:
                enrollment = Enrollment.query.get(enrollment_id)
                if enrollment:
                    student_ids.add(enrollment.student_id)
                
                avg = GradeRepository.calculate_enrollment_average(enrollment_id)
                if avg is not None:
                    averages.append(avg)
                    if avg >= 60:  # Pass threshold (DD and above)
                        passed_count += 1
            
            avg_score = sum(averages) / len(averages) if averages else None
            pass_rate = (passed_count / len(averages) * 100) if averages else None
            
            report.append({
                'course_code': course.course_code,
                'course_name': course.course_name,
                'total_students': len(student_ids),
                'average_grade': float(avg_score) if avg_score else None,
                'pass_rate': float(pass_rate) if pass_rate else None
            })
        
        return report
    
    @staticmethod
    def get_student_transcript_details(student_id):
        """Get student transcript details"""
        from services.student_service import StudentService
        return StudentService.get_transcript_details(student_id)

from repositories import SectionRepository, EnrollmentRepository, GradeRepository, AssessmentTypeRepository
from sqlalchemy import func
from database import db
from models import Grade, Enrollment, ClassSection

class InstructorService:
    @staticmethod
    def get_instructor_sections(instructor_id, page=1, per_page=20):
        return SectionRepository.get_by_instructor(instructor_id, page, per_page)
    
    @staticmethod
    def get_section_enrollments(section_id, page=1, per_page=50):
        return EnrollmentRepository.get_by_section(section_id, page, per_page)
    
    @staticmethod
    def enter_grade(enrollment_id, assessment_type_id, score):
        # Check if grade already exists for this assessment type
        existing = GradeRepository.get_by_assessment_type(enrollment_id, assessment_type_id)
        if existing:
            return GradeRepository.update(existing.grade_id, score=score)
        return GradeRepository.create(enrollment_id, assessment_type_id, score)
    
    @staticmethod
    def update_grade(grade_id, score=None):
        kwargs = {}
        if score is not None:
            kwargs['score'] = score
        return GradeRepository.update(grade_id, **kwargs)
    
    @staticmethod
    def get_course_statistics(course_id):
        """Get course statistics - try stored procedure first, fallback to query"""
        try:
            # Try to call stored procedure if it exists
            result = db.session.execute(
                db.text('CALL GetCourseStatistics(:course_id)'),
                {'course_id': course_id}
            )
            stats = result.fetchone()
            if stats:
                return {
                    'course_id': stats[0] if len(stats) > 0 else course_id,
                    'course_name': stats[1] if len(stats) > 1 else None,
                    'total_students': stats[2] if len(stats) > 2 else 0,
                    'avg_score': float(stats[3]) if len(stats) > 3 and stats[3] else None,
                    'max_score': float(stats[4]) if len(stats) > 4 and stats[4] else None,
                    'min_score': float(stats[5]) if len(stats) > 5 and stats[5] else None
                }
        except Exception as e:
            # Log and continue to fallback
            import logging
            logging.debug(f"Stored procedure not available, using fallback: {str(e)}")
            pass
        
        # Fallback: compute with SQLAlchemy
        try:
            from models import ClassSection, Enrollment, Grade
            
            sections = ClassSection.query.filter_by(course_id=course_id).all()
            if not sections:
                return {
                    'course_id': course_id,
                    'total_students': 0,
                    'avg_score': None,
                    'max_score': None,
                    'min_score': None
                }
            
            section_ids = [s.section_id for s in sections]
            
            # Get all enrollments for all sections (no pagination limit)
            enrollments = Enrollment.query.filter(Enrollment.section_id.in_(section_ids)).all()
            enrollment_ids = [e.enrollment_id for e in enrollments]
            
            if not enrollment_ids:
                return {
                    'course_id': course_id,
                    'total_students': 0,
                    'avg_score': None,
                    'max_score': None,
                    'min_score': None
                }
            
            # Calculate averages per enrollment
            averages = []
            for enrollment_id in enrollment_ids:
                avg = GradeRepository.calculate_enrollment_average(enrollment_id)
                if avg is not None:
                    averages.append(avg)
            
            if not averages:
                return {
                    'course_id': course_id,
                    'total_students': len(enrollments),
                    'avg_score': None,
                    'max_score': None,
                    'min_score': None
                }
            
            return {
                'course_id': course_id,
                'total_students': len(enrollments),
                'avg_score': sum(averages) / len(averages),
                'max_score': max(averages),
                'min_score': min(averages)
            }
        except Exception as e:
            # Log error and return empty stats
            import logging
            logging.error(f"Error getting course statistics for course_id {course_id}: {str(e)}")
            return {
                'course_id': course_id,
                'total_students': 0,
                'avg_score': None,
                'max_score': None,
                'min_score': None
            }
    
    @staticmethod
    def get_section_statistics(section_id):
        """Get statistics for a specific section"""
        try:
            # Get all enrollments without pagination to ensure complete data
            enrollments = EnrollmentRepository.get_all_by_section(section_id)
            enrollment_ids = [e.enrollment_id for e in enrollments]
            
            if not enrollment_ids:
                return {
                    'section_id': section_id,
                    'total_students': 0,
                    'avg_score': None,
                    'max_score': None,
                    'min_score': None
                }
            
            averages = []
            for enrollment_id in enrollment_ids:
                avg = GradeRepository.calculate_enrollment_average(enrollment_id)
                if avg is not None:
                    averages.append(avg)
            
            if not averages:
                return {
                    'section_id': section_id,
                    'total_students': len(enrollment_ids),
                    'avg_score': None,
                    'max_score': None,
                    'min_score': None
                }
            
            return {
                'section_id': section_id,
                'total_students': len(enrollment_ids),
                'avg_score': sum(averages) / len(averages),
                'max_score': max(averages),
                'min_score': min(averages)
            }
        except Exception as e:
            # Log error and return empty stats
            import logging
            logging.error(f"Error getting section statistics for section_id {section_id}: {str(e)}")
            return {
                'section_id': section_id,
                'total_students': 0,
                'avg_score': None,
                'max_score': None,
                'min_score': None
            }

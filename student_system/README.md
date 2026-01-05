# Student System - Flask Web Application

A production-ready web application for managing a student information system with role-based access control (Admin, Instructor, Student).

## Tech Stack

- **Framework**: Flask 3.0.0
- **ORM**: SQLAlchemy 2.0.23
- **Database**: MySQL (pymysql driver)
- **Forms**: WTForms (Flask-WTF)
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5
- **Configuration**: python-dotenv

## Project Structure

```
student_system/
├── app.py                 # Flask application factory
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── seed.py                # Database seeding script
├── .env.example          # Environment variables template
├── controllers/          # Route handlers (blueprints)
│   ├── auth.py
│   ├── admin.py
│   ├── instructor.py
│   ├── student.py
│   └── reports.py
├── models/               # SQLAlchemy models
│   ├── user.py
│   ├── student.py
│   ├── instructor.py
│   ├── course.py
│   ├── semester.py
│   ├── section.py
│   ├── enrollment.py
│   └── grade.py
├── repositories/         # Database operations
│   ├── user_repository.py
│   ├── student_repository.py
│   ├── instructor_repository.py
│   ├── course_repository.py
│   ├── semester_repository.py
│   ├── section_repository.py
│   ├── enrollment_repository.py
│   └── grade_repository.py
├── services/            # Business logic
│   ├── auth_service.py
│   ├── admin_service.py
│   ├── instructor_service.py
│   ├── student_service.py
│   └── report_service.py
├── templates/          # Jinja2 templates
│   ├── base.html
│   ├── auth/
│   ├── admin/
│   ├── instructor/
│   ├── student/
│   └── reports/
└── static/            # Static files (CSS, JS, images)
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- MySQL Server (running on localhost:3306)
- Existing database named "StudentSystem"

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update with your database credentials:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` file:
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YOUR_PASSWORD_HERE
DB_NAME=StudentSystem
SECRET_KEY=change-me-to-a-random-secret-key
```

**Important**: Replace `YOUR_PASSWORD_HERE` with your actual MySQL root password and change `SECRET_KEY` to a random secret string.

### 5. Database Setup

The application uses SQLAlchemy reflection to work with your existing database schema. Ensure your MySQL database "StudentSystem" exists and contains the necessary tables:

- users
- students
- instructors
- courses
- semesters
- sections
- enrollments
- grades

If the tables don't exist, you may need to create them or adjust the models to match your schema.

### 6. Seed the Database (Optional)

To populate the database with sample data:

```bash
python seed.py
```

This will create:
- 1 Admin user (username: `admin`, password: `admin123`)
- 1 Instructor user (username: `instructor1`, password: `instructor123`)
- 1 Student user (username: `student1`, password: `student123`)
- 1 Course, Semester, Section
- 1 Enrollment with sample grades

**⚠️ Security Note**: Change default passwords immediately after first login!

### 7. Run the Application

```bash
flask --app app run --debug
```

Or:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## Features

### Admin Dashboard
- **CRUD Operations**:
  - Manage Students
  - Manage Instructors
  - Manage Courses
- **System Management**:
  - Create Semesters
  - Create Sections
  - Enroll Students into Sections
- **Reports**: View course performance reports

### Instructor Dashboard
- View assigned course sections
- Manage student grades (enter/update grades per assessment type)
- View course and section statistics (average, max, min grades, student count)

### Student Dashboard
- View enrolled courses
- View transcript with:
  - Course averages vs class averages
  - Letter grades
  - Overall GPA

### Reports
- Course Performance Report (all courses with statistics)
- Student Transcript Details

## Creating an Admin User

### Method 1: Using Seed Script
Run the seed script as described above.

### Method 2: Using Python CLI
```python
from app import create_app
from repositories.user_repository import UserRepository

app = create_app()
with app.app_context():
    user = UserRepository.create('admin', 'your_password', 'Admin')
    print(f"Admin user created: {user.username}")
```

### Method 3: Direct Database Insert
```sql
INSERT INTO users (username, password_hash, role) 
VALUES ('admin', '<hashed_password>', 'Admin');
```

Note: For method 3, you'll need to hash the password using Werkzeug's `generate_password_hash()`.

## Database Integration

The application is designed to work with an existing MySQL database. It:

- Uses SQLAlchemy reflection to map existing tables
- Attempts to use stored procedures/functions if they exist:
  - `GetCourseStatistics(course_id)`
  - `CalculateLetterGrade(score)`
- Attempts to use views if they exist:
  - `View_CoursePerformanceReport`
  - `View_StudentTranscriptDetails`
  - `StudentAverage`

If these database objects don't exist, the application falls back to computing results using SQLAlchemy queries.

## Security Features

- Password hashing using Werkzeug
- CSRF protection via Flask-WTF
- Role-based access control
- Parameterized queries (SQL injection prevention)
- Environment variables for sensitive data
- Input validation on all forms

## Logging

Application logs are written to `logs/student_system.log` with rotation (max 10MB per file, 10 backups).

## Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check `.env` file has correct credentials
- Ensure database "StudentSystem" exists
- Test connection: `mysql -u root -p -h 127.0.0.1 StudentSystem`

### Import Errors
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python path includes the project directory

### Template Not Found
- Ensure you're running from the `student_system/` directory
- Check that `templates/` folder exists with all template files

## Development

To run in development mode with auto-reload:

```bash
flask --app app run --debug
```

## Production Deployment

For production:
1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server (e.g., Gunicorn)
3. Set a strong `SECRET_KEY` in `.env`
4. Configure proper database connection pooling
5. Set up HTTPS
6. Configure proper logging

## License

This project is provided as-is for educational purposes.





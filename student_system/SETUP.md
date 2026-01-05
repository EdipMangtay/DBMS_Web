# Quick Setup Guide

## 1. Create .env file

Create a `.env` file in the `student_system/` directory with the following content:

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=Mangtay33
DB_NAME=StudentSystem
SECRET_KEY=change-me-to-a-random-secret-key-please
```

**Important**: Change the `SECRET_KEY` to a random string for production use.

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Run Seed Script (Optional)

To populate the database with sample data:

```bash
python seed.py
```

This creates:
- Admin user: `admin` / `admin123`
- Instructor user: `instructor1` / `instructor123`
- Student user: `student1` / `student123`

## 4. Run the Application

```bash
flask --app app run --debug
```

Or:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Verify the password in `.env` matches your MySQL root password
- Check that the database "StudentSystem" exists

### Import Errors
- Make sure you're in the `student_system/` directory
- Activate your virtual environment
- Run `pip install -r requirements.txt` again

### Template Not Found
- Ensure you're running from the `student_system/` directory
- Check that the `templates/` folder exists





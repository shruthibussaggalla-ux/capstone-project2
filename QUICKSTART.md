# Installation and Quick Start Guide

## System Requirements
- Python 3.8 or higher
- pip package manager
- Modern web browser

## Quick Start (5 minutes)

### Step 1: Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database and tables
python manage.py makemigrations
python manage.py migrate

# Create admin account (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Server runs at: http://localhost:8000

### Step 2: Frontend Setup

Open in your browser:
- `http://localhost:8001/frontend/auth.html` (if running Python HTTP server on port 8001)
- Or directly open the file: `frontend/auth.html` in your browser

### Step 3: Create an Account

1. Click "Register"
2. Fill in your details
3. Click "Register"
4. You'll be logged in automatically
5. Start planning your studies!

## Common Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Access admin panel
# Navigate to http://localhost:8000/admin/
```

## File Locations

- **Backend**: `/backend/smartstudy/`
- **Frontend**: `/frontend/`
- **Database**: `/backend/db.sqlite3`
- **Admin Panel**: `http://localhost:8000/admin/`

## Troubleshooting

### Port Already in Use
```bash
# Change port
python manage.py runserver 8080
```

### Database Errors
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
```

### CORS Issues
- Check that API is at http://localhost:8000
- Update API_BASE_URL in `frontend/js/api.js` if needed

## Next Steps

1. Register a new account
2. Add your courses
3. Create study goals
4. Plan your study sessions
5. Track your progress
6. Check recommendations

Enjoy your study planning journey! 🚀

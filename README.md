# SmartStudy Planner - Full Stack Application

A comprehensive study planning and time management application built with Python Django, SQLite, HTML, CSS, and JavaScript.

## Features

### Core Features
- ✅ User Authentication & Authorization (Registration, Login, Logout)
- ✅ Dashboard with real-time analytics
- ✅ Course Management
- ✅ Study Goal Tracking
- ✅ Study Plans with milestones
- ✅ Task Management with priorities
- ✅ Study Session Scheduling
- ✅ Progress Tracking & Analytics
- ✅ User Profiles with learning preferences
- ✅ Smart Recommendations Engine
- ✅ Responsive UI Design

### Innovative Features
- 🎯 **AI-Powered Recommendations**: Smart suggestions based on study patterns
- 🍅 **Pomodoro Timer Integration**: Built-in timer for focused study sessions
- 📊 **Advanced Analytics**: Weekly/monthly progress tracking with charts
- 📈 **Productivity Score**: Automatic tracking of study effectiveness
- 🔥 **Study Streak Counter**: Motivation through consistency tracking
- 💡 **Learning Style Adaptation**: Personalized study recommendations based on learning style
- 🎓 **Smart Task Prioritization**: Automatic prioritization based on due dates and importance
- 📱 **Fully Responsive**: Works perfectly on desktop, tablet, and mobile devices

## Project Structure

```
capstone-project2/
├── backend/
│   ├── smartstudy/
│   │   ├── __init__.py
│   │   ├── settings.py          (Django configuration)
│   │   ├── urls.py              (URL routing)
│   │   ├── wsgi.py              (WSGI application)
│   │   └── core/
│   │       ├── models.py        (Database models)
│   │       ├── views.py         (API views)
│   │       ├── serializers.py   (DRF serializers)
│   │       ├── urls.py          (API endpoints)
│   │       ├── admin.py         (Admin configuration)
│   │       ├── signals.py       (Django signals)
│   │       ├── tests.py         (Unit tests)
│   │       └── migrations/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── auth.html                (Authentication page)
│   ├── dashboard.html           (Main dashboard)
│   ├── css/
│   │   ├── style.css            (Main styles)
│   │   └── dashboard.css        (Dashboard-specific styles)
│   └── js/
│       ├── api.js               (API client)
│       ├── auth.js              (Authentication logic)
│       └── dashboard.js         (Dashboard logic)
└── README.md
```

## Backend Models

### User Model
- Extends Django's built-in User model
- Email-based authentication

### UserProfile
- Learning style (Visual, Auditory, Reading/Writing, Kinesthetic)
- Daily study goals
- Preferred study time
- Total study hours tracking
- Study streak counter

### Course
- Course information (name, code, instructor, credits)
- Color coding for organization
- Linked to user

### StudyGoal
- Long-term study objectives
- Priority levels (High, Medium, Low)
- Progress tracking (0-100%)
- Linked to courses

### StudyPlan
- Breakdown of study goals into actionable plans
- Timeline and estimated hours
- Resource tracking
- Status management (Not Started, In Progress, Completed, Paused)

### StudySession
- Individual study periods
- Time tracking
- Productivity scoring (1-10)
- Topics covered tracking

### StudyTask
- Specific assignments and tasks
- Priority levels (Critical, High, Medium, Low)
- Status management
- Due date tracking
- Time estimation and tracking

### ProgressLog
- Daily progress tracking
- Study hours per day
- Tasks completed
- Productivity averages

### Recommendation
- AI-powered study recommendations
- Types: Break Reminder, Focus Task, Review Topic, Resource Suggestions, Schedule Optimization
- Confidence scoring
- Expiration dates

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Dashboard
- `GET /api/dashboard/` - Get comprehensive dashboard data

### Courses
- `GET /api/courses/` - List user's courses
- `POST /api/courses/` - Create new course
- `PUT /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course
- `GET /api/courses/by_semester/?semester=...` - Filter by semester

### Study Goals
- `GET /api/goals/` - List goals
- `POST /api/goals/` - Create goal
- `PUT /api/goals/{id}/` - Update goal
- `DELETE /api/goals/{id}/` - Delete goal
- `GET /api/goals/active/` - Get active goals

### Study Plans
- `GET /api/plans/` - List plans
- `POST /api/plans/` - Create plan
- `PUT /api/plans/{id}/` - Update plan
- `DELETE /api/plans/{id}/` - Delete plan
- `GET /api/plans/active/` - Get active plans

### Study Sessions
- `GET /api/sessions/` - List sessions
- `POST /api/sessions/` - Create session
- `PUT /api/sessions/{id}/` - Update session
- `DELETE /api/sessions/{id}/` - Delete session
- `GET /api/sessions/today/` - Get today's sessions
- `GET /api/sessions/upcoming/` - Get upcoming sessions

### Study Tasks
- `GET /api/tasks/` - List tasks
- `POST /api/tasks/` - Create task
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `GET /api/tasks/pending/` - Get pending tasks
- `GET /api/tasks/overdue/` - Get overdue tasks
- `GET /api/tasks/by_priority/?priority=...` - Filter by priority

### User Profile
- `GET /api/profile/` - Get user profile
- `PUT /api/profile/update/` - Update profile

### Progress & Analytics
- `GET /api/progress/` - Get progress logs
- `GET /api/progress/weekly/` - Get weekly progress
- `GET /api/progress/monthly/` - Get monthly progress

### Recommendations
- `GET /api/recommendations/` - Get recommendations
- `POST /api/recommendations/mark_as_read/` - Mark as read

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (admin):**
```bash
python manage.py createsuperuser
```

6. **Start development server:**
```bash
python manage.py runserver
```
Server will run at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Open in browser:**
- Open `auth.html` in your web browser
- Or start a local web server:
```bash
# Python 3
python -m http.server 8001
# Then visit: http://localhost:8001/auth.html
```

## Usage

### First Time Users
1. Go to `/frontend/auth.html`
2. Click "Register" tab
3. Fill in your details (username, email, password, name)
4. Click "Register"
5. You'll be redirected to the dashboard

### Existing Users
1. Go to `/frontend/auth.html`
2. Enter your credentials
3. Click "Login"
4. Access the full dashboard

### Dashboard Features
- **Dashboard**: Overview of all study activities and statistics
- **Courses**: Manage your academic courses
- **Planner**: Create and manage study plans
- **Tasks**: Track individual assignments and tasks
- **Schedule**: View and manage study sessions
- **Analytics**: View progress charts and statistics
- **Recommendations**: Get AI-powered study suggestions
- **Profile**: Update your preferences and learning style

## Key Features Explained

### Pomodoro Timer
- Built-in 25-minute focused study timer
- Helps maintain focus and productivity
- Tracked as study sessions

### Productivity Scoring
- Rate productivity after each study session (1-10)
- Automatic average calculation
- Helps identify peak study times

### Study Streaks
- Tracks consecutive days of study
- Motivational tool for consistency
- Resets if you miss a day

### Smart Recommendations
- Analyzes your study patterns
- Suggests focus areas based on deadlines
- Recommends break times
- Suggests resources for improvement

### Progress Analytics
- Visual charts for study progress
- Weekly/monthly statistics
- Productivity trends
- Task completion rates

## Database Schema

The application uses SQLite with the following main tables:
- `auth_user` - User accounts
- `core_userprofile` - Extended user profile
- `core_course` - Courses
- `core_studygoal` - Study goals
- `core_studyplan` - Study plans
- `core_studysession` - Study sessions
- `core_studytask` - Study tasks
- `core_progresslog` - Progress tracking
- `core_recommendation` - Recommendations

## Security Features

- Token-based authentication (DRF Token)
- CORS protection
- CSRF protection
- Password validation
- Input sanitization
- SQL injection prevention through ORM

## Testing

Run tests with:
```bash
python manage.py test
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Add your domain to `ALLOWED_HOSTS`
- [ ] Generate a new `SECRET_KEY`
- [ ] Configure HTTPS
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Use production WSGI server (Gunicorn, uWSGI)

### Deployment Platforms
- Heroku
- PythonAnywhere
- AWS
- DigitalOcean
- Google Cloud Platform

## Troubleshooting

### CORS Errors
- Ensure backend is running on localhost:8000
- Check CORS_ALLOWED_ORIGINS in settings.py
- Clear browser cache

### Authentication Errors
- Verify token is being saved correctly
- Check browser console for error messages
- Ensure user is registered properly

### API Errors
- Check backend console for error messages
- Verify all required fields are provided
- Check database migrations: `python manage.py migrate`

## Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Video tutorials integration
- [ ] Study group collaboration features
- [ ] Real-time notifications
- [ ] Calendar integration
- [ ] Export reports (PDF, Excel)
- [ ] Dark mode
- [ ] Multi-language support
- [ ] GPA calculator
- [ ] Mock exam feature
- [ ] Study resource library
- [ ] Peer mentoring system

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit and push
5. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@smartstudyplanner.com

## Authors

- Smart Study Development Team

## Acknowledgments

- Django REST Framework
- Chart.js for analytics
- Modern CSS practices
- Open source community

---

**Happy Studying! 📚✨**
#   c a p s t o n e - p r o j e c t 2  
 #   c a p s t o n e - p r o j e c t 2  
 
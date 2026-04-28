# Testing Guide for SmartStudy Planner

## Running Tests

### Unit Tests
```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test core.tests

# Run with verbose output
python manage.py test -v 2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### API Testing

#### Using cURL
```bash
# Registration
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Get Dashboard
curl -H "Authorization: Token <your_token>" \
  http://localhost:8000/api/dashboard/
```

#### Using Postman
1. Import the API collection
2. Set base URL: http://localhost:8000/api
3. Add token to Authorization header
4. Test each endpoint

### Manual Testing Checklist

#### Authentication
- [ ] Register new user
- [ ] Login with credentials
- [ ] Logout successfully
- [ ] Invalid credentials show error
- [ ] Token stored in browser
- [ ] Token used for API calls

#### Dashboard
- [ ] Stats display correctly
- [ ] Upcoming tasks load
- [ ] Today's schedule shows
- [ ] Recommendations appear
- [ ] Navigation works
- [ ] Page refresh maintains state

#### Courses
- [ ] Add course successfully
- [ ] Edit course information
- [ ] Delete course
- [ ] Filter by semester
- [ ] Display in dashboard
- [ ] Color coding works

#### Study Plans
- [ ] Create study plan
- [ ] Link to goal
- [ ] Update status
- [ ] Track progress
- [ ] View tasks in plan
- [ ] View sessions in plan

#### Tasks
- [ ] Create task with priority
- [ ] Set due date
- [ ] Update status
- [ ] Filter by priority
- [ ] Mark complete
- [ ] Display progress bar

#### Study Sessions
- [ ] Schedule session
- [ ] Set duration
- [ ] Rate productivity
- [ ] Add notes
- [ ] View in schedule
- [ ] Complete session

#### Analytics
- [ ] Load weekly chart
- [ ] Load productivity chart
- [ ] Display progress logs
- [ ] Show trends
- [ ] Calculate statistics

#### Profile
- [ ] Update learning style
- [ ] Set daily goals
- [ ] Change preferences
- [ ] Save settings
- [ ] Persist across sessions

### Performance Testing

```bash
# Load testing with Apache Bench
ab -n 100 -c 10 http://localhost:8000/api/dashboard/

# Concurrent user testing
locust -f locustfile.py --host=http://localhost:8000
```

### Database Testing

```bash
# Check database integrity
python manage.py dbshell
sqlite> SELECT COUNT(*) FROM core_course;
sqlite> SELECT COUNT(*) FROM core_studytask;

# Verify migrations
python manage.py showmigrations
```

### Frontend Testing

#### Browser DevTools
- Open Console for JavaScript errors
- Check Network tab for API calls
- Verify Local Storage for token
- Test responsive design

#### Accessibility Testing
- Test keyboard navigation
- Verify color contrast
- Check screen reader compatibility
- Test zoom functionality

### Security Testing

```bash
# Check for SQL injection vulnerability
# Try: admin' OR '1'='1

# CSRF Token Testing
# Ensure CSRF protection enabled

# Password Testing
# Verify password validation
# Test password strength requirements
```

### Load Testing Scenarios

1. **Light Load**: 10 users over 1 minute
2. **Normal Load**: 50 users over 5 minutes
3. **Heavy Load**: 100 users over 10 minutes
4. **Stress Test**: Increase until system breaks

### Error Handling Tests

- [ ] Invalid token returns 401
- [ ] Missing fields return 400
- [ ] Non-existent resource returns 404
- [ ] Database errors handled gracefully
- [ ] Network errors show user message
- [ ] Proper error logging

### Cross-Browser Testing

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers

### Device Testing

- [ ] Desktop (1920x1080)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)
- [ ] Different orientations
- [ ] Touch interactions

### Accessibility Testing

- [ ] WCAG 2.1 compliance
- [ ] Screen reader testing
- [ ] Keyboard navigation
- [ ] Color contrast ratios
- [ ] Alt text for images

## Test Data

### Demo User
- Username: `demouser`
- Password: `demo123456`
- Email: `demo@smartstudy.com`

### Create Sample Data
```bash
python manage.py populate_sample_data
```

## Common Issues & Solutions

### Issue: Tests Fail
**Solution**: 
```bash
# Reset database
python manage.py flush
python manage.py migrate
python manage.py test
```

### Issue: Token Invalid
**Solution**: 
- Clear browser cache
- Logout and login again
- Check token expiration

### Issue: CORS Errors
**Solution**:
- Verify backend URL in api.js
- Check CORS_ALLOWED_ORIGINS in settings
- Clear browser cache

### Issue: Database Locked
**Solution**:
```bash
# Remove old database
rm db.sqlite3
python manage.py migrate
```

## Performance Benchmarks

### Target Metrics
- Dashboard load: < 2 seconds
- API response: < 200ms
- Page render: < 1 second
- Database query: < 100ms

### Monitoring Commands
```bash
# Database query time
python manage.py shell
>>> from django.db import connection
>>> from django.test.utils import override_settings
>>> from core.models import *
>>> print(connection.queries)
```

## Continuous Integration

### GitHub Actions Configuration
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python manage.py test
```

## Coverage Targets

- Overall: 80%+
- Models: 90%+
- Views: 85%+
- Serializers: 80%+
- Utils: 75%+

## Regression Testing

### Critical Workflows to Test
1. User registration and first login
2. Creating and completing a study plan
3. Task management workflow
4. Dashboard analytics accuracy
5. Profile preferences saving

---

**Last Updated**: April 2024
**Version**: 1.0.0

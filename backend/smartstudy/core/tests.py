"""
Django tests for SmartStudy Planner.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Course, StudyGoal, StudyPlan, StudyTask


class CourseAPITestCase(APITestCase):
    """Test cases for Course API."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            user=self.user,
            name='Python 101',
            code='CS101',
            credit_hours=3,
            instructor='Dr. Smith',
            semester='Spring 2024'
        )

    def test_list_courses(self):
        """Test listing user's courses."""
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_course(self):
        """Test creating a new course."""
        data = {
            'name': 'Data Science 101',
            'code': 'CS201',
            'credit_hours': 4,
            'instructor': 'Dr. Johnson',
            'semester': 'Spring 2024'
        }
        response = self.client.post('/api/courses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)


class AuthAPITestCase(APITestCase):
    """Test cases for Authentication API."""

    def test_user_registration(self):
        """Test user registration."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_user_login(self):
        """Test user login."""
        User.objects.create_user(username='testuser', password='testpass123')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

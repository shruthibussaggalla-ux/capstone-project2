"""
Management command to populate sample data for demonstration
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from core.models import (
    Course, StudyGoal, StudyPlan, StudySession, StudyTask, UserProfile
)


class Command(BaseCommand):
    help = 'Populate database with sample data for demonstration'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create a test user
        user, created = User.objects.get_or_create(
            username='demouser',
            defaults={
                'email': 'demo@smartstudy.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )

        if created:
            user.set_password('demo123456')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
        else:
            self.stdout.write(f'User {user.username} already exists')

        # Create user profile
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'learning_style': 'VISUAL',
                'daily_study_goal_hours': 3,
                'preferred_study_time': '09:00',
                'notification_enabled': True,
                'weekly_report_enabled': True,
            }
        )

        # Create sample courses
        courses_data = [
            {
                'name': 'Python Programming',
                'code': 'CS101',
                'instructor': 'Dr. John Smith',
                'credit_hours': 4,
                'semester': 'Spring 2024',
                'color': '#3498db'
            },
            {
                'name': 'Data Structures',
                'code': 'CS201',
                'instructor': 'Dr. Jane Doe',
                'credit_hours': 3,
                'semester': 'Spring 2024',
                'color': '#2ecc71'
            },
            {
                'name': 'Web Development',
                'code': 'WEB101',
                'instructor': 'Prof. Mike Johnson',
                'credit_hours': 3,
                'semester': 'Spring 2024',
                'color': '#e74c3c'
            },
        ]

        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                user=user,
                code=course_data['code'],
                defaults=course_data
            )
            courses.append(course)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.name}'))

        # Create sample study goals
        for course in courses:
            goal, created = StudyGoal.objects.get_or_create(
                user=user,
                course=course,
                title=f'Master {course.name}',
                defaults={
                    'description': f'Complete all topics in {course.name} and achieve an A grade',
                    'target_grade': 'A',
                    'priority': 'HIGH',
                    'target_date': timezone.now().date() + timedelta(days=90),
                    'progress_percentage': 0,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created goal for {course.name}'))

        # Create sample study plans
        goals = StudyGoal.objects.filter(user=user)
        for goal in goals:
            plan, created = StudyPlan.objects.get_or_create(
                user=user,
                goal=goal,
                title=f'Study Plan for {goal.title}',
                defaults={
                    'description': f'Comprehensive study plan to achieve the goal of {goal.title}',
                    'status': 'IN_PROGRESS',
                    'start_date': timezone.now().date(),
                    'end_date': timezone.now().date() + timedelta(days=60),
                    'estimated_hours': 40,
                    'actual_hours': 12,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created plan: {plan.title}'))

        # Create sample study tasks
        plans = StudyPlan.objects.filter(user=user)
        priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        for i, plan in enumerate(plans):
            for j in range(3):
                task, created = StudyTask.objects.get_or_create(
                    user=user,
                    plan=plan,
                    course=plan.goal.course,
                    title=f'Task {j+1}: {plan.goal.title}',
                    defaults={
                        'description': f'Complete assignment #{j+1} for {plan.goal.course.name}',
                        'priority': priorities[j % len(priorities)],
                        'status': 'TODO' if j == 0 else ('IN_PROGRESS' if j == 1 else 'COMPLETED'),
                        'due_date': timezone.now().date() + timedelta(days=7 + j*3),
                        'estimated_hours': 2 + j,
                        'actual_hours': 1.5 + j if j <= 1 else 2 + j,
                        'completed': j == 2,
                    }
                )
                if created:
                    self.stdout.write(f'Created task: {task.title}')

        # Create sample study sessions
        sessions_data = [
            {
                'title': 'Python Fundamentals Review',
                'duration_minutes': 60,
                'productivity_score': 8,
                'offset_days': 0
            },
            {
                'title': 'Data Structures Practice',
                'duration_minutes': 90,
                'productivity_score': 9,
                'offset_days': 1
            },
            {
                'title': 'Web Development HTML/CSS',
                'duration_minutes': 120,
                'productivity_score': 7,
                'offset_days': 2
            },
            {
                'title': 'Problem Solving Session',
                'duration_minutes': 75,
                'productivity_score': 8,
                'offset_days': 3
            },
        ]

        course_index = 0
        plan_index = 0
        for session_data in sessions_data:
            session, created = StudySession.objects.get_or_create(
                user=user,
                plan=plans[plan_index % len(plans)],
                course=courses[course_index % len(courses)],
                scheduled_date=timezone.now().date() - timedelta(days=session_data['offset_days']),
                title=session_data['title'],
                defaults={
                    'description': f'Study session: {session_data["title"]}',
                    'status': 'COMPLETED',
                    'scheduled_time': timezone.now().time(),
                    'duration_minutes': session_data['duration_minutes'],
                    'topics_covered': 'Core concepts and practice problems',
                    'productivity_score': session_data['productivity_score'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created session: {session.title}'))
            course_index += 1
            plan_index += 1

        self.stdout.write(self.style.SUCCESS('✓ Sample data created successfully!'))
        self.stdout.write(f'Test user credentials: username=demouser, password=demo123456')

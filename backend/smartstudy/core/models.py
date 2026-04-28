"""
Django models for SmartStudy Planner application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class Course(models.Model):
    """Model for academic courses."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    credit_hours = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(12)])
    instructor = models.CharField(max_length=200)
    semester = models.CharField(max_length=50, default='Spring 2024')
    color = models.CharField(max_length=7, default='#3498db')  # hex color
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'semester'])]

    def __str__(self):
        return f"{self.code} - {self.name}"


class StudyGoal(models.Model):
    """Model for long-term study goals."""
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_goals')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=300)
    description = models.TextField()
    target_grade = models.CharField(max_length=5, default='A')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    target_date = models.DateField()
    completed = models.BooleanField(default=False)
    progress_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', 'target_date']

    def __str__(self):
        return self.title


class StudyPlan(models.Model):
    """Model for study plans and schedules."""
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('PAUSED', 'Paused'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_plans')
    goal = models.ForeignKey(StudyGoal, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    start_date = models.DateField()
    end_date = models.DateField()
    estimated_hours = models.FloatField(validators=[MinValueValidator(0.5)])
    actual_hours = models.FloatField(validators=[MinValueValidator(0)], default=0)
    resources_needed = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def progress_percentage(self):
        if self.estimated_hours > 0:
            return min(int((self.actual_hours / self.estimated_hours) * 100), 100)
        return 0


class StudySession(models.Model):
    """Model for individual study sessions with time tracking."""
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name='sessions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='study_sessions')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    duration_minutes = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(480)])
    topics_covered = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    productivity_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date', '-scheduled_time']

    def __str__(self):
        return f"{self.title} - {self.scheduled_date}"


class StudyTask(models.Model):
    """Model for individual study tasks and assignments."""
    PRIORITY_CHOICES = [
        ('CRITICAL', 'Critical'),
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('BLOCKED', 'Blocked'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_tasks')
    plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name='tasks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    due_date = models.DateField()
    estimated_hours = models.FloatField(validators=[MinValueValidator(0.5)])
    actual_hours = models.FloatField(validators=[MinValueValidator(0)], default=0)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', '-priority']

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """Extended user profile for SmartStudy Planner."""
    LEARNING_STYLE_CHOICES = [
        ('VISUAL', 'Visual'),
        ('AUDITORY', 'Auditory'),
        ('READING', 'Reading/Writing'),
        ('KINESTHETIC', 'Kinesthetic'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='smartstudy_profile')
    learning_style = models.CharField(max_length=20, choices=LEARNING_STYLE_CHOICES, default='VISUAL')
    daily_study_goal_hours = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(12)], default=2)
    preferred_study_time = models.TimeField(default='09:00')
    notification_enabled = models.BooleanField(default=True)
    weekly_report_enabled = models.BooleanField(default=True)
    total_study_hours = models.FloatField(default=0)
    streak_days = models.IntegerField(default=0)
    last_study_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class ProgressLog(models.Model):
    """Model to track user progress over time."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_logs')
    date = models.DateField(auto_now_add=True)
    study_hours_today = models.FloatField(validators=[MinValueValidator(0)], default=0)
    tasks_completed_today = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    average_productivity_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
    total_study_hours = models.FloatField(validators=[MinValueValidator(0)], default=0)
    courses_count = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Recommendation(models.Model):
    """Model for AI-powered study recommendations."""
    RECOMMENDATION_TYPE_CHOICES = [
        ('BREAK', 'Take a Break'),
        ('FOCUS', 'Focus on Priority'),
        ('REVIEW', 'Review Previous Topics'),
        ('RESOURCES', 'Suggested Resources'),
        ('SCHEDULE', 'Schedule Recommendation'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPE_CHOICES)
    title = models.CharField(max_length=300)
    description = models.TextField()
    action_item = models.CharField(max_length=500, blank=True)
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

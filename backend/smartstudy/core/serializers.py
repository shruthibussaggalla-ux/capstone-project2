"""
Serializers for SmartStudy Planner API.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Course, StudyGoal, StudyPlan, StudySession,
    StudyTask, UserProfile, ProgressLog, Recommendation
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'learning_style', 'daily_study_goal_hours', 'preferred_study_time',
                  'notification_enabled', 'weekly_report_enabled', 'total_study_hours',
                  'streak_days', 'last_study_date', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'total_study_hours', 'streak_days')


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'code', 'description', 'credit_hours', 'instructor',
                  'semester', 'color', 'task_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_task_count(self, obj):
        return obj.tasks.count()


class StudyGoalSerializer(serializers.ModelSerializer):
    """Serializer for StudyGoal model."""
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = StudyGoal
        fields = ('id', 'course', 'course_name', 'title', 'description', 'target_grade',
                  'priority', 'target_date', 'completed', 'progress_percentage',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class StudyTaskSerializer(serializers.ModelSerializer):
    """Serializer for StudyTask model."""
    course_name = serializers.CharField(source='course.name', read_only=True)
    days_until_due = serializers.SerializerMethodField()

    class Meta:
        model = StudyTask
        fields = ('id', 'plan', 'course', 'course_name', 'title', 'description',
                  'priority', 'status', 'due_date', 'estimated_hours', 'actual_hours',
                  'completed', 'completion_date', 'days_until_due', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_days_until_due(self, obj):
        from datetime import date
        delta = obj.due_date - date.today()
        return delta.days


class StudySessionSerializer(serializers.ModelSerializer):
    """Serializer for StudySession model."""
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = StudySession
        fields = ('id', 'plan', 'course', 'course_name', 'title', 'description',
                  'status', 'scheduled_date', 'scheduled_time', 'duration_minutes',
                  'topics_covered', 'notes', 'productivity_score',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class StudyPlanSerializer(serializers.ModelSerializer):
    """Serializer for StudyPlan model."""
    goal_title = serializers.CharField(source='goal.title', read_only=True)
    tasks = StudyTaskSerializer(many=True, read_only=True)
    sessions = StudySessionSerializer(many=True, read_only=True)

    class Meta:
        model = StudyPlan
        fields = ('id', 'goal', 'goal_title', 'title', 'description', 'status',
                  'start_date', 'end_date', 'estimated_hours', 'actual_hours',
                  'resources_needed', 'tasks', 'sessions', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProgressLogSerializer(serializers.ModelSerializer):
    """Serializer for ProgressLog model."""
    class Meta:
        model = ProgressLog
        fields = ('id', 'date', 'study_hours_today', 'tasks_completed_today',
                  'average_productivity_score', 'total_study_hours', 'courses_count')
        read_only_fields = ('id', 'date')


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for Recommendation model."""
    class Meta:
        model = Recommendation
        fields = ('id', 'recommendation_type', 'title', 'description', 'action_item',
                  'confidence_score', 'is_read', 'created_at', 'expires_at')
        read_only_fields = ('id', 'created_at')


class DashboardSerializer(serializers.Serializer):
    """Serializer for dashboard analytics data."""
    total_study_hours = serializers.FloatField()
    tasks_completed = serializers.IntegerField()
    tasks_pending = serializers.IntegerField()
    courses_active = serializers.IntegerField()
    average_productivity = serializers.FloatField()
    streak_days = serializers.IntegerField()
    upcoming_tasks = StudyTaskSerializer(many=True)
    today_sessions = StudySessionSerializer(many=True)
    recent_progress = ProgressLogSerializer(many=True)

"""
Django admin configuration for SmartStudy Planner.
"""
from django.contrib import admin
from .models import (
    Course, StudyGoal, StudyPlan, StudySession, 
    StudyTask, UserProfile, ProgressLog, Recommendation
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'instructor', 'credit_hours', 'user', 'semester')
    list_filter = ('semester', 'created_at')
    search_fields = ('name', 'code', 'instructor')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StudyGoal)
class StudyGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'target_grade', 'priority', 'target_date', 'completed')
    list_filter = ('priority', 'completed', 'target_date')
    search_fields = ('title', 'course__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal', 'status', 'start_date', 'end_date', 'estimated_hours')
    list_filter = ('status', 'start_date')
    search_fields = ('title', 'goal__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'scheduled_date', 'status', 'duration_minutes')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('title', 'course__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StudyTask)
class StudyTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'priority', 'status', 'due_date', 'completed')
    list_filter = ('priority', 'status', 'due_date')
    search_fields = ('title', 'course__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'learning_style', 'daily_study_goal_hours', 'streak_days', 'total_study_hours')
    list_filter = ('learning_style', 'notification_enabled')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProgressLog)
class ProgressLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'study_hours_today', 'tasks_completed_today', 'average_productivity_score')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('date',)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recommendation_type', 'user', 'confidence_score', 'is_read', 'created_at')
    list_filter = ('recommendation_type', 'is_read', 'created_at')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at',)

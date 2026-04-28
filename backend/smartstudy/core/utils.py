"""
Utilities for SmartStudy Planner
Advanced features and helper functions
"""

from datetime import datetime, timedelta
from django.utils import timezone
from .models import StudySession, ProgressLog, Recommendation, StudyTask, StudyGoal


class AIRecommendationEngine:
    """
    AI-powered recommendation engine for SmartStudy Planner
    Analyzes user patterns and generates personalized recommendations
    """

    def __init__(self, user):
        self.user = user

    def generate_recommendations(self):
        """Generate recommendations based on user activity patterns"""
        recommendations = []

        # Check if user should take a break
        break_rec = self.check_break_recommendation()
        if break_rec:
            recommendations.append(break_rec)

        # Check priority focus
        priority_rec = self.check_priority_recommendation()
        if priority_rec:
            recommendations.append(priority_rec)

        # Check review recommendation
        review_rec = self.check_review_recommendation()
        if review_rec:
            recommendations.append(review_rec)

        # Check resource recommendation
        resource_rec = self.check_resource_recommendation()
        if resource_rec:
            recommendations.append(resource_rec)

        # Check schedule optimization
        schedule_rec = self.check_schedule_recommendation()
        if schedule_rec:
            recommendations.append(schedule_rec)

        return recommendations

    def check_break_recommendation(self):
        """Recommend a break if user has studied too long"""
        today = timezone.now().date()
        today_sessions = StudySession.objects.filter(
            user=self.user,
            scheduled_date=today,
            status='COMPLETED'
        )
        total_minutes = sum(session.duration_minutes for session in today_sessions)

        if total_minutes > 180:  # More than 3 hours
            return Recommendation.objects.create(
                user=self.user,
                recommendation_type='BREAK',
                title='Time for a Break!',
                description='You have studied for over 3 hours today. Consider taking a 15-20 minute break to refresh your mind.',
                action_item='Take a walk or have a snack',
                confidence_score=0.95,
                expires_at=timezone.now() + timedelta(hours=2)
            )
        return None

    def check_priority_recommendation(self):
        """Recommend focusing on high-priority overdue tasks"""
        today = timezone.now().date()
        overdue_high_priority = StudyTask.objects.filter(
            user=self.user,
            due_date__lt=today,
            priority__in=['CRITICAL', 'HIGH'],
            completed=False
        ).count()

        if overdue_high_priority > 0:
            return Recommendation.objects.create(
                user=self.user,
                recommendation_type='FOCUS',
                title='Focus on Priority Tasks',
                description=f'You have {overdue_high_priority} high-priority overdue tasks. It\'s time to focus on these.',
                action_item='Start with the task closest to deadline',
                confidence_score=0.9,
                expires_at=timezone.now() + timedelta(hours=4)
            )
        return None

    def check_review_recommendation(self):
        """Recommend reviewing topics"""
        try:
            profile = self.user.smartstudy_profile
            if profile.learning_style in ['VISUAL', 'KINESTHETIC']:
                return Recommendation.objects.create(
                    user=self.user,
                    recommendation_type='REVIEW',
                    title='Time to Review',
                    description='Based on your learning style, regular review sessions help strengthen memory.',
                    action_item='Review notes from 3-5 days ago',
                    confidence_score=0.7,
                    expires_at=timezone.now() + timedelta(days=1)
                )
        except:
            pass
        return None

    def check_resource_recommendation(self):
        """Recommend study resources"""
        goals = StudyGoal.objects.filter(
            user=self.user,
            completed=False
        ).count()

        if goals > 0:
            return Recommendation.objects.create(
                user=self.user,
                recommendation_type='RESOURCES',
                title='Enhance Your Learning',
                description='Check out recommended resources like videos, articles, and practice problems.',
                action_item='Visit Khan Academy or YouTube for supplemental content',
                confidence_score=0.65,
                expires_at=timezone.now() + timedelta(days=1)
            )
        return None

    def check_schedule_recommendation(self):
        """Optimize study schedule"""
        try:
            profile = self.user.smartstudy_profile
            today = timezone.now().date()
            today_minutes = StudySession.objects.filter(
                user=self.user,
                scheduled_date=today,
                status='COMPLETED'
            ).aggregate(total=models.Sum('duration_minutes'))['total'] or 0

            if today_minutes < profile.daily_study_goal_hours * 60 * 0.5:
                return Recommendation.objects.create(
                    user=self.user,
                    recommendation_type='SCHEDULE',
                    title='Schedule Study Session',
                    description='You are falling behind your daily study goal. Consider scheduling another study session.',
                    action_item=f'Schedule a {int((profile.daily_study_goal_hours * 60) / 2)}-minute session',
                    confidence_score=0.8,
                    expires_at=timezone.now() + timedelta(hours=1)
                )
        except:
            pass
        return None


class ProductivityAnalyzer:
    """
    Analyzes user productivity patterns and provides insights
    """

    def __init__(self, user):
        self.user = user

    def get_productivity_score(self, days=7):
        """Calculate average productivity score for recent sessions"""
        since_date = timezone.now().date() - timedelta(days=days)
        sessions = StudySession.objects.filter(
            user=self.user,
            status='COMPLETED',
            scheduled_date__gte=since_date,
            productivity_score__isnull=False
        )

        if not sessions.exists():
            return 0

        avg_score = sessions.aggregate(models.Avg('productivity_score'))['productivity_score__avg']
        return round(avg_score, 1) if avg_score else 0

    def get_peak_study_hours(self):
        """Identify user's most productive study hours"""
        sessions = StudySession.objects.filter(
            user=self.user,
            status='COMPLETED',
            productivity_score__isnull=False
        )

        if not sessions.exists():
            return None

        # Group by hour and calculate average productivity
        hour_productivity = {}
        for session in sessions:
            hour = session.scheduled_time.hour
            if hour not in hour_productivity:
                hour_productivity[hour] = {'total': 0, 'count': 0}
            hour_productivity[hour]['total'] += session.productivity_score
            hour_productivity[hour]['count'] += 1

        # Calculate averages
        peak_hour = None
        peak_score = 0
        for hour, data in hour_productivity.items():
            avg = data['total'] / data['count']
            if avg > peak_score:
                peak_score = avg
                peak_hour = hour

        return peak_hour

    def get_study_consistency(self):
        """Calculate study consistency (number of consecutive study days)"""
        try:
            profile = self.user.smartstudy_profile
            return profile.streak_days
        except:
            return 0

    def get_recommendations_for_improvement(self):
        """Get actionable recommendations for improving productivity"""
        recommendations = []

        # Check peak hours
        peak_hour = self.get_peak_study_hours()
        if peak_hour is not None:
            recommendations.append(
                f'You are most productive at {peak_hour:02d}:00. Schedule important tasks during this time.'
            )

        # Check session length
        sessions = StudySession.objects.filter(
            user=self.user,
            status='COMPLETED'
        ).aggregate(avg_duration=models.Avg('duration_minutes'))

        if sessions['avg_duration'] and sessions['avg_duration'] > 120:
            recommendations.append(
                'Your average session is quite long. Consider breaking it into smaller Pomodoro sessions.'
            )

        return recommendations


class StudyStreakTracker:
    """
    Tracks user study streaks and maintains consistency metrics
    """

    def __init__(self, user):
        self.user = user

    def update_streak(self):
        """Update user's study streak"""
        try:
            profile = self.user.smartstudy_profile
        except:
            return

        today = timezone.now().date()

        # Check if user studied today
        today_sessions = StudySession.objects.filter(
            user=self.user,
            scheduled_date=today,
            status='COMPLETED'
        )

        if today_sessions.exists():
            yesterday = today - timedelta(days=1)

            # Check if user studied yesterday
            yesterday_sessions = StudySession.objects.filter(
                user=self.user,
                scheduled_date=yesterday,
                status='COMPLETED'
            )

            if yesterday_sessions.exists():
                # Continue streak
                profile.streak_days += 1
            else:
                # Start new streak
                profile.streak_days = 1

            profile.last_study_date = today
            profile.save()

    def reset_streak_if_needed(self):
        """Reset streak if user missed a day"""
        try:
            profile = self.user.smartstudy_profile
        except:
            return

        if profile.last_study_date:
            today = timezone.now().date()
            days_since = (today - profile.last_study_date).days

            if days_since > 1:
                profile.streak_days = 0
                profile.save()


def calculate_goal_progress(goal):
    """Calculate progress percentage for a study goal"""
    tasks = StudyTask.objects.filter(plan__goal=goal)
    if not tasks.exists():
        return 0

    completed = tasks.filter(completed=True).count()
    return int((completed / tasks.count()) * 100)


from django.db import models as django_models

"""
Signals for SmartStudy Planner.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, ProgressLog, StudySession
from datetime import datetime


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created."""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=StudySession)
def update_progress_log(sender, instance, created, **kwargs):
    """Update progress log when study session is created or updated."""
    if instance.status == 'COMPLETED':
        today = datetime.now().date()
        progress_log, _ = ProgressLog.objects.get_or_create(user=instance.user, date=today)

        # Update study hours
        total_minutes = StudySession.objects.filter(
            user=instance.user,
            scheduled_date=today,
            status='COMPLETED'
        ).values_list('duration_minutes', flat=True)
        progress_log.study_hours_today = sum(total_minutes) / 60

        # Save the log
        progress_log.save()

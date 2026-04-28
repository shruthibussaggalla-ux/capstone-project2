"""
URL configuration for core app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, StudyGoalViewSet, StudyPlanViewSet,
    StudySessionViewSet, StudyTaskViewSet, UserProfileViewSet,
    ProgressLogViewSet, RecommendationViewSet,
    dashboard, register, login, logout
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'goals', StudyGoalViewSet, basename='goal')
router.register(r'plans', StudyPlanViewSet, basename='plan')
router.register(r'sessions', StudySessionViewSet, basename='session')
router.register(r'tasks', StudyTaskViewSet, basename='task')
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'progress', ProgressLogViewSet, basename='progress')
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard, name='dashboard'),
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
]

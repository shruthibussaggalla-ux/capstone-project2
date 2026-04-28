"""
Views for SmartStudy Planner API.
"""
from rest_framework import viewsets, status, generics, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import (
    Course, StudyGoal, StudyPlan, StudySession,
    StudyTask, UserProfile, ProgressLog, Recommendation
)
from .serializers import (
    CourseSerializer, StudyGoalSerializer, StudyPlanSerializer,
    StudySessionSerializer, StudyTaskSerializer, UserProfileSerializer,
    ProgressLogSerializer, RecommendationSerializer, UserSerializer, DashboardSerializer
)


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for managing courses."""
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code', 'instructor']

    def get_queryset(self):
        return Course.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def by_semester(self, request):
        """Get courses filtered by semester."""
        semester = request.query_params.get('semester')
        if semester:
            queryset = self.get_queryset().filter(semester=semester)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "Semester parameter required"}, status=status.HTTP_400_BAD_REQUEST)


class StudyGoalViewSet(viewsets.ModelViewSet):
    """ViewSet for managing study goals."""
    serializer_class = StudyGoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'course__name']

    def get_queryset(self):
        return StudyGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active (not completed) goals."""
        queryset = self.get_queryset().filter(completed=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudyPlanViewSet(viewsets.ModelViewSet):
    """ViewSet for managing study plans."""
    serializer_class = StudyPlanSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'goal__title']

    def get_queryset(self):
        return StudyPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active study plans."""
        queryset = self.get_queryset().filter(status__in=['NOT_STARTED', 'IN_PROGRESS'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudySessionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing study sessions."""
    serializer_class = StudySessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'course__name']

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's study sessions."""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(scheduled_date=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming study sessions."""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(scheduled_date__gte=today, status__in=['SCHEDULED', 'ACTIVE']).order_by('scheduled_date')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudyTaskViewSet(viewsets.ModelViewSet):
    """ViewSet for managing study tasks."""
    serializer_class = StudyTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'course__name']

    def get_queryset(self):
        return StudyTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending tasks."""
        queryset = self.get_queryset().filter(status__in=['TODO', 'IN_PROGRESS']).order_by('due_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue tasks."""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(due_date__lt=today, completed=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        """Get tasks filtered by priority."""
        priority = request.query_params.get('priority')
        if priority:
            queryset = self.get_queryset().filter(priority=priority).order_by('due_date')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "Priority parameter required"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ViewSet):
    """ViewSet for managing user profiles."""
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get user profile."""
        try:
            profile = request.user.smartstudy_profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Update user profile."""
        try:
            profile = request.user.smartstudy_profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgressLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing progress logs."""
    serializer_class = ProgressLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProgressLog.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def weekly(self, request):
        """Get weekly progress."""
        days_back = 7
        since_date = timezone.now().date() - timedelta(days=days_back)
        queryset = self.get_queryset().filter(date__gte=since_date).order_by('date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def monthly(self, request):
        """Get monthly progress."""
        days_back = 30
        since_date = timezone.now().date() - timedelta(days=days_back)
        queryset = self.get_queryset().filter(date__gte=since_date).order_by('date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RecommendationViewSet(viewsets.ViewSet):
    """ViewSet for managing recommendations."""
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get active recommendations."""
        recommendations = Recommendation.objects.filter(
            user=request.user,
            expires_at__gte=timezone.now()
        ).order_by('-created_at')
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        """Mark recommendation as read."""
        rec_id = request.data.get('id')
        try:
            rec = Recommendation.objects.get(id=rec_id, user=request.user)
            rec.is_read = True
            rec.save()
            return Response({"status": "marked as read"})
        except Recommendation.DoesNotExist:
            return Response({"error": "Recommendation not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    """Get comprehensive dashboard analytics."""
    user = request.user
    today = timezone.now().date()

    # Calculate statistics
    total_study_hours = StudySession.objects.filter(
        user=user, status='COMPLETED'
    ).aggregate(total=Sum('duration_minutes'))['total'] or 0
    total_study_hours = total_study_hours / 60

    tasks_completed = StudyTask.objects.filter(user=user, completed=True).count()
    tasks_pending = StudyTask.objects.filter(user=user, completed=False).count()
    courses_active = Course.objects.filter(user=user).count()

    productivity_scores = StudySession.objects.filter(
        user=user, status='COMPLETED', productivity_score__isnull=False
    ).aggregate(avg=Avg('productivity_score'))['avg'] or 0

    # Get user profile
    try:
        profile = user.smartstudy_profile
        streak_days = profile.streak_days
    except UserProfile.DoesNotExist:
        streak_days = 0

    # Get upcoming tasks
    upcoming_tasks = StudyTask.objects.filter(
        user=user, completed=False, due_date__gte=today
    ).order_by('due_date')[:5]

    # Get today's sessions
    today_sessions = StudySession.objects.filter(
        user=user, scheduled_date=today
    )

    # Get recent progress
    since_date = today - timedelta(days=7)
    recent_progress = ProgressLog.objects.filter(
        user=user, date__gte=since_date
    ).order_by('-date')

    data = {
        'total_study_hours': round(total_study_hours, 2),
        'tasks_completed': tasks_completed,
        'tasks_pending': tasks_pending,
        'courses_active': courses_active,
        'average_productivity': round(productivity_scores, 1),
        'streak_days': streak_days,
        'upcoming_tasks': StudyTaskSerializer(upcoming_tasks, many=True).data,
        'today_sessions': StudySessionSerializer(today_sessions, many=True).data,
        'recent_progress': ProgressLogSerializer(recent_progress, many=True).data,
    }

    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user."""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    if not username or not email or not password:
        return Response(
            {"error": "Username, email, and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    # Create user profile
    UserProfile.objects.create(user=user)

    # Create token
    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'user': UserSerializer(user).data,
        'token': token.key
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return token."""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'user': UserSerializer(user).data,
        'token': token.key
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user by deleting token."""
    request.user.auth_token.delete()
    return Response({"status": "logged out"})

from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import (
    Category, Building, Room, QRLocation, Route,
    UserProfile, SearchHistory, VisitedLocation,
    Feedback, Notice
)
from .serializers import (
    CategorySerializer, BuildingSerializer, RoomSerializer,
    QRLocationSerializer, RouteSerializer, UserProfileSerializer,
    SearchHistorySerializer, VisitedLocationSerializer,
    FeedbackSerializer, NoticeSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.AllowAny]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('building', 'category').all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]


class QRLocationViewSet(viewsets.ModelViewSet):
    queryset = QRLocation.objects.select_related('room', 'room__building', 'room__category').all()
    serializer_class = QRLocationSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        # Enables building full image URL in serializer
        return {'request': self.request}


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related('start_room', 'end_room').all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user').prefetch_related('favorites').all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.select_related('user', 'room').all()
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VisitedLocationViewSet(viewsets.ModelViewSet):
    queryset = VisitedLocation.objects.select_related('user', 'room').all()
    serializer_class = VisitedLocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('user', 'room').all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializer
    permission_classes = [permissions.AllowAny]

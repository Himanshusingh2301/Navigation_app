from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, BuildingViewSet, RoomViewSet, QRLocationViewSet,
    RouteViewSet, UserProfileViewSet, SearchHistoryViewSet,
    VisitedLocationViewSet, FeedbackViewSet, NoticeViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'buildings', BuildingViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'qrlocations', QRLocationViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'search-history', SearchHistoryViewSet)
router.register(r'visited-locations', VisitedLocationViewSet)
router.register(r'feedbacks', FeedbackViewSet)
router.register(r'notices', NoticeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

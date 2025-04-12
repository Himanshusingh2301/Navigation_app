from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, BuildingViewSet, RoomViewSet, QRLocationViewSet,
    RouteViewSet, UserProfileViewSet, SearchHistoryViewSet,
    VisitedLocationViewSet, FeedbackViewSet, NoticeViewSet,search_rooms, search_buildings,get_shortest_path_room,get_shortest_path_building
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
    path('roomsearch/', search_rooms, name='search-rooms'),
    path('buildingsearch/', search_buildings, name='search-rooms'),
    path('roomshortest-path/', get_shortest_path_room, name='shortest-path'),
    path('buildingshortest-path/', get_shortest_path_building, name='shortest-path'),
]

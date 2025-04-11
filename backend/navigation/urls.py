from django.urls import path
from .views import *

urlpatterns = [
    path('buildings/', BuildingListCreate.as_view(), name='building-list'),
    path('rooms/', RoomListCreate.as_view(), name='room-list'),
    path('qr-locations/', QRLocationListCreate.as_view(), name='qr-list'),
    path('feedback/', FeedbackListCreate.as_view(), name='feedback-list'),
    path('notices/', NoticeListCreate.as_view(), name='notice-list'),
    # Add more as needed
]

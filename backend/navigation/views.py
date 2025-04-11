from rest_framework import generics
from .models import Building, Room, QRLocation, UserProfile, Route, SearchHistory, VisitedLocation, Feedback, Notice
from .serializers import *

# Example: List + Create Views
class BuildingListCreate(generics.ListCreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class RoomListCreate(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class QRLocationListCreate(generics.ListCreateAPIView):
    queryset = QRLocation.objects.all()
    serializer_class = QRLocationSerializer

class FeedbackListCreate(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class NoticeListCreate(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

# You can also add RetrieveUpdateDestroy views if needed for admin side

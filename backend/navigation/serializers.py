from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Building, Room, QRLocation, Route,
    UserProfile, SearchHistory, VisitedLocation,
    Feedback, Notice
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['id', 'name', 'location', 'latitude', 'longitude']

class RoomSerializer(serializers.ModelSerializer):
    building_id = serializers.PrimaryKeyRelatedField(queryset=Building.objects.all(), source='building')
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', allow_null=True)

    class Meta:
        model = Room
        fields = [
            'id', 'name', 'building_id', 'floor', 'description',
            'category_id', 'latitude', 'longitude'
        ]

class QRLocationSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    qr_image_url = serializers.SerializerMethodField()

    class Meta:
        model = QRLocation
        fields = ['id', 'code', 'room', 'qr_image_url']

    def get_qr_image_url(self, obj):
        request = self.context.get('request')
        if obj.qr_image and request:
            return request.build_absolute_uri(obj.qr_image.url)
        return None

class RouteSerializer(serializers.ModelSerializer):
    start_room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='start_room')
    end_room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='end_room')
    start_room_name = serializers.CharField(source='start_room.name', read_only=True)
    end_room_name = serializers.CharField(source='end_room.name', read_only=True)

    class Meta:
        model = Route
        fields = [
            'id', 'start_room_id', 'end_room_id',
            'start_room_name', 'end_room_name',
            'path_description'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    favorites = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), many=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'favorites']

class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    room = RoomSerializer()

    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'room', 'timestamp']

class VisitedLocationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    room = RoomSerializer()

    class Meta:
        model = VisitedLocation
        fields = ['id', 'user', 'room', 'visited_at']

class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    room = RoomSerializer()

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'room', 'message', 'created_at']

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'created_at']

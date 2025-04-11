from django.contrib import admin
from .models import (
    Category, Building, Room, QRLocation, Route,
    UserProfile, SearchHistory, VisitedLocation,
    Feedback, Notice
)

import qrcode
from io import BytesIO
import base64
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'latitude', 'longitude')
    search_fields = ('name', 'location')
    list_filter = ['location']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'building', 'floor', 'category', 'latitude', 'longitude')
    list_filter = ('building', 'floor', 'category')
    search_fields = ('name', 'building__name', 'category__name')


@admin.register(QRLocation)
class QRLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'code', 'qr_preview')
    search_fields = ('room__name', 'code')

    def qr_preview(self, obj):
        qr = qrcode.make(obj.code)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return format_html(f'<img src="data:image/png;base64,{img_str}" width="80" height="80" />')

    qr_preview.short_description = 'QR Preview'


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_room', 'end_room')
    search_fields = ('start_room__name', 'end_room__name')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'room__name')


@admin.register(VisitedLocation)
class VisitedLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'visited_at')
    list_filter = ('visited_at',)
    search_fields = ('user__username', 'room__name')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'room__name', 'message')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title', 'content')

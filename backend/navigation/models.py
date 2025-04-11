from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files import File
import qrcode

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Building(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)   # For map marker
    longitude = models.FloatField(null=True, blank=True)  # For map marker

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=200)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    floor = models.IntegerField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)   # Optional marker override
    longitude = models.FloatField(null=True, blank=True)  # Optional marker override

    def __str__(self):
        return f"{self.name} - {self.building.name}"

class QRLocation(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"QR for {self.room.name}"

    def save(self, *args, **kwargs):
        if not self.qr_image or 'update_fields' in kwargs:
            qr = qrcode.make(self.code)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            self.qr_image.save(f"{self.room.name}_qr.png", File(buffer), save=False)
        super().save(*args, **kwargs)

class Route(models.Model):
    start_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='route_start', null=True, blank=True)
    end_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='route_end', null=True, blank=True)
    path_description = models.TextField()

    def __str__(self):
        return f"{self.start_room.name if self.start_room else 'Unknown'} to {self.end_room.name if self.end_room else 'Unknown'}"

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('visitor', 'Visitor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    favorites = models.ManyToManyField(Room, blank=True)

    def __str__(self):
        return self.user.username

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class VisitedLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    visited_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


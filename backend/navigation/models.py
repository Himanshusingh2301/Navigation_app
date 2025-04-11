from django.db import models
from django.contrib.auth.models import User

# Category of a room/location (e.g., Lab, Hall, Washroom)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Building on campus
class Building(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location_coordinates = models.CharField(max_length=255)  # e.g., "28.6139,77.2090"

    def __str__(self):
        return self.name


# Room or place inside a building
class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., "Room 101"
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    floor = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    location_coordinates = models.CharField(max_length=255)  # For precise location

    def __str__(self):
        return f"{self.name} ({self.building.name})"


# Images for rooms
class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image of {self.room.name}"


# Extend user model for role & favorites
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('visitor', 'Visitor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    favorite_rooms = models.ManyToManyField(Room, blank=True)

    def __str__(self):
        return self.user.username


# QR code locations mapped to a room
class QRLocation(models.Model):
    qr_code_data = models.CharField(max_length=255, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"QR for {self.room.name}"


# Route between two rooms (optional: for internal pathfinding)
class Route(models.Model):
    source = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='route_from')
    destination = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='route_to')
    path_description = models.TextField()  # Optional: instructions like "Take stairs, turn right..."

    def __str__(self):
        return f"{self.source.name} → {self.destination.name}"


# Keep search history of users
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} searched {self.query}"


# Log of locations visited (if needed for tracking)
class VisitedLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} visited {self.room.name}"


# Feedback form for user suggestions or problems
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback by {self.user.username if self.user else 'Anonymous'}"


# Admin or management notices related to buildings
class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    target_building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active_until = models.DateTimeField()

    def __str__(self):
        return self.title

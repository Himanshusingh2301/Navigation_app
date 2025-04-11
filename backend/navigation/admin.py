from django.contrib import admin
from .models import Building, Room, QRLocation, UserProfile, Route, SearchHistory, VisitedLocation, Feedback, Notice

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(QRLocation)
admin.site.register(UserProfile)
admin.site.register(Route)
admin.site.register(SearchHistory)
admin.site.register(VisitedLocation)
admin.site.register(Feedback)
admin.site.register(Notice)

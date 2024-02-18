from .models import Room, RoomStatus
from django.contrib import admin

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'password', 'end_date', 'owner',)

admin.site.register(Room, RoomAdmin)

admin.site.register(RoomStatus)

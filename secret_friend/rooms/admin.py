from django.contrib import admin

from users.models import EmailVerification
from .models import Room, RoomStatus, SubChat


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'password', 'end_date', 'owner',)

admin.site.register(Room, RoomAdmin)

admin.site.register(RoomStatus)
admin.site.register(SubChat)

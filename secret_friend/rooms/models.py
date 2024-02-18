from django.db import models
from django.contrib.auth.models import User

class RoomStatus(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
class Room(models.Model):
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=255, blank=True, null=True)  # Increase the maximum length
    status = models.ForeignKey(RoomStatus, on_delete=models.CASCADE)
    end_date = models.DateField(auto_now_add=False, blank=True, null=True)  # This will store a date, not datetime
    participants = models.ManyToManyField(User, related_name='invited_rooms', blank=True)
    invited_emails = models.EmailField(max_length=1024, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_password_correct(self, input_password):
        return input_password == self.password

    def __str__(self):
        return self.name

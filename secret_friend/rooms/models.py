from django.core.mail import send_mail
from django.db import models


from config import settings


class RoomStatus(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
class Room(models.Model):
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=255, blank=True, null=True)  # Increase the maximum length
    status = models.ForeignKey(RoomStatus, on_delete=models.CASCADE)
    end_date = models.DateField(auto_now_add=False, blank=True, null=True)  # This will store a date, not datetime
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rooms_participated')
    invited_emails = models.EmailField(max_length=1024, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rooms_owned')

    def send_invitation_email(self, recipient_emails):
        game_name = self.name
        end_date = self.end_date
        owner = self.owner.email
        send_mail(
            subject=f'You just were invited to {game_name}',
            message=f'Hi,'
                    f'{owner} just invited you to {game_name}. If you are ready to join, just click here. Game ends on {end_date}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_emails,
        )

    def is_password_correct(self, input_password):
        return input_password == self.password

    def participation(self, request, input_password):
        if self.is_password_correct(input_password):
            self.participants.add(request.user)
            self.save()
            return self.participants

    def take_participation(self, request):
        self.participants.add(request.user)
        self.save()
        return self.participants

    def leave_participation(self, request):
        self.participants.remove(request.user)
        self.save()
        return self.participants

    def __str__(self):
        return self.name

class SubChat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subchats')
    date = models.DateField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'Chat for {self.room.name}'

import random
import uuid

from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from config import settings
from users.models import Wish


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
    invitation_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def send_invitation_email(self, recipient_emails):
        game_name = self.name
        end_date = self.end_date
        owner = self.owner.email
        invitation_link = f'http://127.0.0.1:8000/rooms/invite/{self.invitation_token}/?email={",".join(recipient_emails)}'
        send_mail(
            subject=f'You just were invited to {game_name}',
            message=f'Hi,'
                    f'{owner} just invited you to {game_name}. If you are ready to join, just click here {invitation_link}. Game ends on {end_date}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_emails,  # Передаем список адресов как recipient_list
        ) # Передаем список адресов как recipient_list

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

    def start_game(self):
        participants = list(self.participants.all())
        if len(participants) < 2:
            return
        random.shuffle(participants)
        for i, giver in enumerate(participants):
            game_name = self.name
            wishes = Wish.objects.filter(parent=giver)
            receiver = participants[(i+ 1) % len(participants)]
            html_message = render_to_string('mails/start_game.html',
                                            {'giver': giver, 'receiver': receiver, 'wishes': wishes})
            send_mail(
                subject=f'Game {game_name} started',
                message=strip_tags(html_message),  # Преобразование HTML в текст
                html_message=html_message,  # HTML содержимое письма
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[giver.email],
            )

    def __str__(self):
        return self.name

class SubChat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subchats')
    date = models.DateField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'Chat for {self.room.name}'

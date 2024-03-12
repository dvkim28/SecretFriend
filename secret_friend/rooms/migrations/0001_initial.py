# Generated by Django 5.0.2 on 2024-03-04 21:24

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('invited_emails', models.EmailField(blank=True, max_length=1024)),
                ('invitation_token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms_owned', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(related_name='rooms_participated', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.roomstatus')),
            ],
        ),
        migrations.CreateModel(
            name='SubChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('text', models.TextField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subchats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

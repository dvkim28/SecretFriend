# Generated by Django 5.0.2 on 2024-02-17 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='password',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

# Generated by Django 5.0.4 on 2024-05-24 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grooming_service', '0022_appointment_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='image',
        ),
    ]

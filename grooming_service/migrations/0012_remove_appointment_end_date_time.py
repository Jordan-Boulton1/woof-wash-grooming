# Generated by Django 5.0.4 on 2024-05-12 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grooming_service', '0011_alter_appointment_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='end_date_time',
        ),
    ]
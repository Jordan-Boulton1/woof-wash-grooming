# Generated by Django 5.0.4 on 2024-05-01 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grooming_service', '0004_user_groups_user_is_superuser_user_last_login_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]

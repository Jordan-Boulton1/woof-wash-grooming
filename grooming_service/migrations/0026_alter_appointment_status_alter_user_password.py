# Generated by Django 5.0.4 on 2024-06-02 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grooming_service', '0025_service_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.IntegerField(choices=[(1, 'booked'), (2, 'completed')], default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]

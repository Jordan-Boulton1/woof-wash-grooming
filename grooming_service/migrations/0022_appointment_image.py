# Generated by Django 5.0.4 on 2024-05-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grooming_service', '0021_rename_price_service_vary_price1_service_vary_price2'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='image',
            field=models.ImageField(default='media/images/rlbpt7uaqhxanu59ro9r', upload_to='images/'),
        ),
    ]

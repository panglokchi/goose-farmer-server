# Generated by Django 5.1.7 on 2025-03-21 04:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goose_farmer_game', '0003_verificationtoken_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationtoken',
            name='expiry',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 3, 21, 14, 10, 50, 862971, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]

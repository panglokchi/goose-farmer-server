# Generated by Django 5.1.7 on 2025-03-22 17:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goose_farmer_game', '0005_birdtype_player_alter_verificationtoken_expiry_bird'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationtoken',
            name='expiry',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 3, 23, 3, 50, 44, 364401, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]

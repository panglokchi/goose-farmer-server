# Generated by Django 5.1.7 on 2025-03-24 14:21

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goose_farmer_game', '0008_rename_max_weight_female_birdtype_max_weight_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={},
        ),
        migrations.AlterModelManagers(
            name='player',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='player',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='verificationtoken',
            name='expiry',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 3, 25, 0, 20, 46, 247638, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]

# Generated by Django 5.1.7 on 2025-03-21 01:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationToken',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expiry', models.DateTimeField(blank=True, default=datetime.timedelta(seconds=36000), null=True)),
                ('key', models.CharField(default='26859397f0ae', primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

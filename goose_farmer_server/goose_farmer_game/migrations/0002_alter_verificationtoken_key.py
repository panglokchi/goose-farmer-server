# Generated by Django 5.1.7 on 2025-03-21 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goose_farmer_game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationtoken',
            name='key',
            field=models.CharField(default='230f75ad1313', primary_key=True, serialize=False),
        ),
    ]

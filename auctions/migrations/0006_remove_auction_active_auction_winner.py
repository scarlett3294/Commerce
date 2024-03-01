# Generated by Django 5.0.1 on 2024-02-27 18:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='active',
        ),
        migrations.AddField(
            model_name='auction',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_auctions', to=settings.AUTH_USER_MODEL),
        ),
    ]

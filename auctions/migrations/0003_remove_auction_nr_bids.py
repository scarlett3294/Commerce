# Generated by Django 5.0.1 on 2024-02-26 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_auction_bid_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='nr_bids',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-03-29 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_current_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='current_bidder',
            field=models.CharField(default='', max_length=100),
        ),
    ]
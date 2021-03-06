# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-23 16:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('monitoree', '0002_auto_20170323_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Scraped'), (3, 'Ignore')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monitoring',
            name='monitoring_url',
            field=models.CharField(default=datetime.datetime(2017, 3, 23, 16, 18, 22, 923630, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Scraped'), (3, 'Ignore')], max_length=1),
        ),
        migrations.AlterField(
            model_name='monitoring',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Scraped'), (3, 'Ignore')], max_length=1),
        ),
        migrations.AlterField(
            model_name='url',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Scraped'), (3, 'Ignore')], max_length=1),
        ),
    ]

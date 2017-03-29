# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-27 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoree', '0011_auto_20170327_0741'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SubCategory',
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Scraped'), (3, 'Ignore')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.IntegerField(max_length=6),
        ),
        migrations.AlterField(
            model_name='item',
            name='is_scrapped',
            field=models.IntegerField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Scraped'), (3, 'Ignore')], max_length=3),
        ),
        migrations.AlterField(
            model_name='monitoring',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Scraped'), (3, 'Ignore')], max_length=3),
        ),
        migrations.AlterField(
            model_name='url',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Scraped'), (3, 'Ignore')], max_length=4),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-29 04:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoree', '0017_auto_20170329_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_name_1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='image_name_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='image_name_3',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='image_name_4',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='image_name_5',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

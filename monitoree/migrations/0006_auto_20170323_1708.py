# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-23 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoree', '0005_auto_20170323_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='attr',
        ),
        migrations.RemoveField(
            model_name='category',
            name='attr_val',
        ),
        migrations.RemoveField(
            model_name='category',
            name='tag',
        ),
        migrations.AddField(
            model_name='monitoring',
            name='attr',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='monitoring',
            name='attr_val',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='monitoring',
            name='tag',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]

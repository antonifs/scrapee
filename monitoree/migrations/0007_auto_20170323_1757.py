# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-23 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoree', '0006_auto_20170323_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoring',
            name='attr_child',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='monitoring',
            name='attr_val_child',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='monitoring',
            name='tag_child',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]

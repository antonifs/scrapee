# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-29 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoree', '0018_auto_20170329_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='directory',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
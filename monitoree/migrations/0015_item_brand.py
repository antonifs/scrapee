# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-28 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoree', '0014_auto_20170327_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='brand',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
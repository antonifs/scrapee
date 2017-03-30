# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-27 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoree', '0010_category_category_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('monitoree.category',),
        ),
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.IntegerField(default=1, max_length=2),
        ),
    ]
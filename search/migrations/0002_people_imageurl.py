# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-15 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='imageurl',
            field=models.CharField(default='', max_length=1024),
        ),
    ]
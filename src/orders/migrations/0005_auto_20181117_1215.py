# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-17 06:45
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20181117_1142'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('order', django.db.models.manager.Manager()),
            ],
        ),
    ]

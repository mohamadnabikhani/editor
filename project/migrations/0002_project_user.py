# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-25 12:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='user_on_project', to=settings.AUTH_USER_MODEL),
        ),
    ]

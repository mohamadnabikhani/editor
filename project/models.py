# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models import *
from editor.settings import AUTH_USER_MODEL

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    users = models.ManyToManyField(User, related_name='user_on_project', blank=True)
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'owner',)



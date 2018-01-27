# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def create_user(self, data, request):
        user = User(**data)
        # print user
        password = data.pop('password', None)
        user.password = make_password(password)
        user.save()
        return user


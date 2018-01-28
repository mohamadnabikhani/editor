# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import binascii
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
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

# class Token(models.Model):
#     """
#     The default authorization token model.
#     """
#     key = models.CharField(_("Key"), max_length=40, primary_key=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+',
#         on_delete=models.CASCADE, verbose_name=_("User"))
#     concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
#     created = models.DateTimeField(_("Created"), auto_now_add=True)
#
#     class Meta:
#         # Work around for a bug in Django:
#         # https://code.djangoproject.com/ticket/19422
#         #
#         # Also see corresponding ticket:
#         # https://github.com/encode/django-rest-framework/issues/705
#         abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
#         verbose_name = _("Token")
#         verbose_name_plural = _("Tokens")
#
#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super(Token, self).save(*args, **kwargs)
#
#     def generate_key(self):
#         return binascii.hexlify(os.urandom(20)).decode()
#
#     def __str__(self):
#         return self.key



# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from django.http import HttpResponse
from serializers import *
from csrf import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate as auth_authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.db import IntegrityError
from users.models import *
from models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from django.shortcuts import render

# Create your views here.

class Singup(APIView):


    permission_classes = ()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(Singup, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # user = request.user
        user = User()
        serializer_data = Input_SingUpSerializer(data=request.data,context={'request': request})
        serializer_data.is_valid(raise_exception=True)
        data = serializer_data.data
        try:
            user = user.create_user(data=data,request=request)
            # user = auth_authenticate(request=request, username=user.username, password=user.password)
            auth_login(request=request, user=user)

            output_serialized = Output_UserSerializer(instance=user)
            return Response({"user": output_serialized.data}, status=200)
        except IntegrityError:
            return Response("username already exists!", status=406)


class Login(APIView):
    permission_classes = ()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(Login, self).dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        # user = request.user

        serializer_data = Input_LoginSerializer(data=request.data,context={'request': request})
        serializer_data.is_valid(raise_exception=True)
        data = serializer_data.data
        # user = User(**data)
        username = data.pop('username', None)
        password = data.pop('password', None)
        user = auth_authenticate(request=request, username=username, password=password)

        if user is not None:
            auth_login(request=request, user=user)
            output_serialized = Output_UserSerializer(instance=user)
            return Response({"user": output_serialized.data}, status=200)
        else:
            if len(User.objects.filter(username=username)) == 0:
                return Response({"user not exist"}, status=400)

            else:
                return Response({"password is wrong"}, status=400)



class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(Logout, self).dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        user = request.user
        auth_logout(request=request)
        return Response("user is logged out", status=200)



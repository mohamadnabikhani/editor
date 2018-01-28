# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from csrf import CsrfExemptSessionAuthentication
from rest_framework.authentication import  BasicAuthentication

from django.http import HttpResponse
from serializers import *
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

class ProjectListOwn(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        # request_data = request.GET
        if not user.is_anonymous:
            response = Project.objects.filter(owner=user)
            serializer_data = Output_ProjectList(data = response, many=True, context={'request': request})
            serializer_data.is_valid()
            data = serializer_data.data
            return Response(data, status=200)
        else:
            return Response("not logged in", status=400)


class ProjectListJoint(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        # request_data = request.GET
        if not user.is_anonymous:
            response = Project.objects.filter(users=user)
            serializer_data = Output_ProjectList(data = response, many=True, context={'request': request})
            serializer_data.is_valid()
            data = serializer_data.data
            return Response(data, status=200)
        else:
            return Response("not logged in", status=400)


class AddUserProject(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(AddUserProject, self).dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer_data = Input_AddRemoveUser(data=request.data,context={'request': request})
        serializer_data.is_valid(raise_exception=True)
        project_id = serializer_data.validated_data["project_id"]
        project = Project.objects.filter(id=project_id).first()

        new_user = serializer_data.validated_data["user"]
        newuser = User.objects.filter(username=new_user)

        if not newuser:
            # user = user.first()
            return Response("username is not exit", status=400)
        else:
            newuserObj = newuser.first()

        if not user.is_anonymous:
            if user == project.owner:
                project = project.users.add(newuserObj)

                return Response("user added", status=200)
            else:
                return Response("user is not project owner", status=400)
        else:
            return Response('not logged in', status=400)



    def delete(self, request, *args, **kwargs):
        user = request.user
        serializer_data = Input_AddRemoveUser(data=request.data, context={'request': request})
        serializer_data.is_valid(raise_exception=True)
        project_id = serializer_data.validated_data["project_id"]
        project = Project.objects.filter(id=project_id).first()

        new_user = serializer_data.validated_data["user"]
        newuser = User.objects.filter(username=new_user)

        if not newuser:
            # user = user.first()
            return Response("username is not exit", status=400)
        else:
            newuserObj = newuser.first()

        if not user.is_anonymous:
            if user == project.owner:
                project.users.remove(newuserObj)

                return Response("user removed", status=200)
            else:
                return Response("user is not project owner", status=400)
        else:
            return Response('not logged in', status=400)


class LeaveProject(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(LeaveProject, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer_data = Input_LeaveProject(data=request.data,context={'request': request})
        serializer_data.is_valid(raise_exception=True)
        project_id = serializer_data.validated_data["project_id"]
        project = Project.objects.filter(id=project_id).first()

        if not user.is_anonymous:
            if user in project.users.all():
                project.users.remove(user)

                return Response("user left", status=200)
            else:
                return Response("user is not project owner", status=400)
        else:
            return Response('not logged in', status=400)


class DeleteProject(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(DeleteProject, self).dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer_data = Input_DeleteProject(data=request.data,context={'request': request})
        serializer_data.is_valid(raise_exception=True)
        project_id = serializer_data.validated_data["project_id"]
        project = Project.objects.filter(id=project_id).first()


        if not user.is_anonymous:
            if user == project.owner:

                project.delete()

                return Response("project delete", status=200)
            else:
                return Response("user is not project owner", status=400)
        else:
            return Response('not logged in', status=400)


# @method_decorator(csrf_exempt, name='dispatch')
class CreateProject(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(CreateProject, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer_data = Input_CreateProject(data=request.data, context={'request': request})
        serializer_data.is_valid(raise_exception=True)
        project_name = serializer_data.validated_data["name"]

        if not user.is_anonymous:
            project = Project(name=project_name, owner=user)
            project.save()



            return Response("project created", status=200)

        else:
            return Response('not logged in', status=400)


class ListPojectParticipator(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer_data = Input_PojectParticipator(data=request.GET, context={'request': request})
        serializer_data.is_valid(raise_exception=True)
        project_id = serializer_data.validated_data["project_id"]
        # request_data = request.GET
        if not user.is_anonymous:
            response = Project.objects.filter(id=project_id)
            serializer_data = Output_PojectParticipator(data = response, many=True, context={'request': request})
            serializer_data.is_valid()
            data = serializer_data.data
            return Response(data, status=200)
        else:
            return Response("not logged in", status=400)



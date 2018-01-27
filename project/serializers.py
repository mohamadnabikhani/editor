from models import *
from rest_framework import serializers
from users.serializers import Output_UserSerializer


class Output_ProjectList(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', )


class Output_PojectParticipator(serializers.ModelSerializer):
    users = Output_UserSerializer(read_only=True,many=True)
    class Meta:
        model = Project
        fields = ('id', 'name','users')

class Input_PojectParticipator(serializers.Serializer):
    project_id = serializers.IntegerField(required=True)

class Input_AddRemoveUser(serializers.Serializer):
    user = serializers.CharField(max_length=100,required=True)
    project_id = serializers.IntegerField(required=True)


class Input_DeleteProject(serializers.Serializer):
    project_id = serializers.IntegerField(required=True)


class Input_LeaveProject(serializers.Serializer):
    project_id = serializers.IntegerField(required=True)


class Input_CreateProject(serializers.Serializer):
    name = serializers.CharField(max_length=100)

from models import *
from rest_framework import serializers



class Output_UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)

class Input_SingUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100,required=True)
    password = serializers.CharField(max_length=100, required=True)


class Input_LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100,required=True)
    password = serializers.CharField(max_length=100, required=True)

from rest_framework import serializers
from . import models


class SystemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SystemUser
        fields = ('id', 'name')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ('id', 'sender', 'receiver', 'subject', 'message', 'created', 'is_read')

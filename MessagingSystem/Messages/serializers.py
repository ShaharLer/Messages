from rest_framework import serializers
from . import models


class SystemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SystemUser
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super(MessageSerializer, self).to_representation(instance)
        representation['created'] = instance.created.strftime('%d-%m-%Y')
        return representation

    class Meta:
        model = models.Message
        fields = '__all__'
        depth = 1

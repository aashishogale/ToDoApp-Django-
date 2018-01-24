from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.response import Response
from django.views.defaults import bad_request
from rest_framework import status
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'password','email')
        extra_kwargs = {'email': {'required':True},'password': {'required':True}}
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
      
        user.save()

        return user

# def validate(self, data):
#         """
#         Check that the start is before the stop.
#         """
#         if data['start'] > data['finish']:
#             raise serializers.ValidationError("finish must occur after start")
#         return data
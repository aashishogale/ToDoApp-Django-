from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.response import Response
from django.views.defaults import bad_request
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Notes

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'password','email')
        extra_kwargs = {'email': {'required':True},'password': {'required':True}}
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active=False
        user.save()

        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    # default_error_messages = {
    #     'inactive_account': _('User account is disabled.'),
    #     'invalid_credentials': _('Unable to login with provided credentials.')
    # }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        print(attrs)
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        print(self.error_messages)
  
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])

class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token",)



class NoteSerializer(serializers.ModelSerializer):
    # id = serializers.PrimaryKeyRelatedField(read_only=True)
    # def get_queryset(self, values):
    #     return Notes.objects.filter(mergefields__contained_by=['django']) #This must an array of keys from the Research object's JSON field
    # items = SerializerMethodField('get_items')
    class Meta:
        model = Notes
        # fields = "__all__"
        fields = ('id','title','description', 'date_created','owner','isArchived','isPinned','isTrashed')
       
    # def get_items(self, container):
    #     items = Notes.objects.filter()  # Whatever your query may be
    #     serializer = ItemSerializer(instance=items, many=True)
    #     return serializer.data
    # def create(self, validated_data):
    #     note= Notes.notemanager.create(**validated_data)
        
        

    #     return note


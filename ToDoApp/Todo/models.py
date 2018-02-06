from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from rest_framework_jwt.settings import api_settings
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import datetime

fs = FileSystemStorage(location='/media/photos')

class Notes(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=2000)
    description=models.TextField(max_length=2000)
    date_created=models.DateTimeField(auto_now_add=True)
    isArchived=models.BooleanField(default=False)
    isPinned=models.BooleanField(default=False)
    isTrashed=models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    reminder = models.DateTimeField(default=timezone.now)
    objects=models.Manager()
    color=models.CharField(max_length=2000,default="#ffffff")
  
    def __str__(self):
        return 

    def __unicode__(self):
        return 

class Profile(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    
    photo = models.ImageField(blank=True,upload_to='userimages/%m-%Y/')
    objects=models.Manager()

    def __str__(self):
        return 

    def __unicode__(self):
        return 

class Collaborator(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='collaboratednoteowner')
    shareduser=models.ForeignKey(User,on_delete=models.CASCADE)
    note=models.ForeignKey(Notes,on_delete=models.CASCADE)
    objects=models.Manager()
    def __str__(self):
        return 

    def __unicode__(self):
        return 
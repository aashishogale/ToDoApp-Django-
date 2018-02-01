from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from rest_framework_jwt.settings import api_settings
from django.urls import reverse

class Notes(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=2000)
    description=models.TextField(max_length=2000)
    date_created=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return 

    def __unicode__(self):
        return 


class Note(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=2000)
    description=models.CharField(max_length=2000)
    date_created=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return 

    def __unicode__(self):
        return 
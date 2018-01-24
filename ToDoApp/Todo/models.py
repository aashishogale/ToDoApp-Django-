from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=2000)
    description=models.CharField(max_length=2000)
    date_created=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return 

    def __unicode__(self):
        return 


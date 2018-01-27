from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from rest_framework_jwt.settings import api_settings

class Notes(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=2000)
    description=models.CharField(max_length=2000)
    date_created=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return 

    def __unicode__(self):
        return 

@receiver(post_save, sender=User)
def send_mail(sender, **kwargs):
    user=User.objects.get(id=kwargs.get('instance').id)
    request = None
    from django.core.mail import EmailMessage
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    jwttoken = jwt_encode_handler(payload)
    url = 'http://127.0.0.1:8000/ToDoApp/verifytoken/'+jwttoken
    email = EmailMessage('Subject', url, to=['ashtest1947@gmail.com'])
    email.send()
   
    print(url)
from celery import shared_task, task
from django.conf import settings
from django.shortcuts import reverse
import logging
from .models import Notes
from django.contrib.auth.models import User

logging.basicConfig(level=logging.DEBUG,   format='%(asctime)s %(levelname)-8s %(message)s',

                    datefmt='%Y-%m-%d %H:%M:%S',)
logger = logging.getLogger(__name__)


@shared_task
def sendmail(useremail, jwttoken):

    logger.warning("mail sender entered")
   

    url = settings.BASE_URL + \
        reverse('todo:verifytoken', args=[jwttoken])

    message = 'Dear User, </br> Please verify your email by clicking on the below link ' + \
        url + ' </br></br> Thank you, </br> Todo Team'

 
    # from django.core.mail import send_mail
    # try:
    # from django.core.mail import EmailMessage
    # email = EmailMessage('Subject', message,['ashtest1947@gmail.com'])
    # print("herer")
    # email.send(fail_silently=False)
    from django.core.mail import get_connection, send_mail

    conn = get_connection(backend='django.core.mail.backends.smtp.EmailBackend')
    # send_mail(subject, message, fromname, tolist, fail_silently=False, connection=conn)
    send_mail(
            'Subject here',
            message,
            # settings.EMAIL_HOST_USER,
            'ashtest1947@gmail.com',
            ['ashtest1947@gmail.com'],
            fail_silently=False,
            connection=conn
        )

    print(url)

    return url

@shared_task
def print2():
    print("enter")
    
# user=User.objects.all()

@shared_task
def deleteArchivedNotes():
    logger.warning("archived notes entered")
    # users=User.objects.all()
    # user = ''
    # for user1 in users:
    #     user = user1.username
    #     print(user1.username)
    logger.warning("users got")
    notes=Notes.objects.all()
    logger.info("notes gotten")
    for note in notes:
        if(note.isArchived==False):
            note.delete()
            logger.warning("notes deleted successfully")

    return True
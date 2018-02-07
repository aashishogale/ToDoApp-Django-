from django.contrib.auth.models import User
from django.http import Http404, request, HttpResponseRedirect
from django.shortcuts import render, reverse, render, redirect

from rest_framework import status, generics, serializers, viewsets
# from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.cache import never_cache
from Todo.serializers import ProfileSerializer, UserSerializer, UserLoginSerializer, TokenSerializer, NoteSerializer, CollaboratorSerializer
from Todo.serializers import LabelSerializer
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework_jwt.settings import api_settings
from random import randint
from .models import Notes, Collaborator, Profile, Labels
from django.core.mail import EmailMessage
from django.core.cache import cache
from pyee import EventEmitter
import asyncio
from functools import wraps
import redis
from django.db.models import Q
from itertools import chain
# from rest_framework import
from django.conf import settings
import logging
import time
from django.db.models import OuterRef, Subquery

# Get an instance of a logger()

logging.basicConfig(filename='/home/bridgelabz/TodoAppDjango/ToDoApp/logger.log', level=logging.DEBUG,   format='%(asctime)s %(levelname)-8s %(message)s',

                    datefmt='%Y-%m-%d %H:%M:%S',)
logger = logging.getLogger(__name__)


# Create your views here.
otp = {}
ee = EventEmitter()


def startlogin(request):
    return render(request, 'Todo/index.html')


class UserRegisterView(CreateAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            user = serializer.instance
            payload = jwt_payload_handler(user)
            jwttoken = jwt_encode_handler(payload)
        # token, created = Token.objects.get_or_create(user=user)
        # data = serializer.data
            #data["token"] = token.key

            #headers = self.get_success_headers(serializer.data)
            print("inside register")

            ee.emit('sendmail', user.email, jwttoken)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
           # token, _ = Token.objects.get_or_create(user=user)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            jwttoken = jwt_encode_handler(payload)

            cache = redis.StrictRedis(host='localhost', decode_responses=True)
            cache.set(jwttoken, user.username)
            logger.warning("logged in successfully")
            data = {
                "username": user.username,
                "id": user.id,
                "token": jwttoken

            }
            return Response(
                # data=TokenSerializer(token).data,
                data=data,
                status=status.HTTP_200_OK,

            )
        else:
            logger.warning(serializer.errors)
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @csrf_exempt
    def delete(self, request, format=None):
        logger.warning("logged out successfully")
        logout(request)
        return Response(status=status.HTTP_200_OK)


class VerifyToken(GenericAPIView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        try:
            print(self.kwargs['token'])
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
            payload = jwt_decode_handler(self.kwargs['token'])
            print(payload)
            username = jwt_get_username_from_payload(payload)
            print(username)
            # user=User.objects.filter(username=username)
            # print(user)
            # users=User.objects.all()
            # print(users[10:])

            User.objects.filter(username=username).update(is_active=True)
            return redirect('http://127.0.0.1:8000/ToDoApp/')
        except Exception as e:
            status = status.HTTP_401_UNAUTHORIZED
            msg = "not authenticated"

        # print(request.get_absolute_url(self))


class GenerateOTP(GenericAPIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        useremail = data['email']
        print(useremail)
        user = User.objects.get(email=useremail)
        users = User.objects.all()
        if user in users:

            randomno = randint(1000, 9999)

            otp[str(randomno)] = user.email
            print(otp[str(randomno)])
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            jwttoken = jwt_encode_handler(payload)
            email = EmailMessage('Subject', str(randomno),
                                 to=['ashtest1947@gmail.com'])
            email.send()
            return Response(
                # # data=TokenSerializer(token).data,
                data=jwttoken,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class CheckOTP(GenericAPIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        randomno = data['otp']
        print(randomno)
        print(otp)
        useremail = otp[str(randomno)]
        print(useremail)
        user = User.objects.get(email=useremail)
        users = User.objects.all()
        if user in users:
            return Response(
                # # data=TokenSerializer(token).data,
                # data= jwttoken,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLogoutView(GenericAPIView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        jwttoken = request.META.get('HTTP_TOKEN')

        cache = redis.StrictRedis(host='localhost', decode_responses=True)
        cache.delete(jwttoken)
        return Response(
            # # data=TokenSerializer(token).data,
            # data= jwttoken,
            status=status.HTTP_200_OK
        )


class ChangePassword(GenericAPIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print(request.META.get('HTTP_TOKEN'))
        data = request.data
        password = data['password']
        print(password)
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
        payload = jwt_decode_handler(request.META.get('HTTP_TOKEN'))
        print(payload)
        username = jwt_get_username_from_payload(payload)
        print(username)
        users = User.objects.all()
        user = User.objects.get(username=username)
        # if user in users:
        User.objects.filter(username=username).update(password=password)
        return Response(
            # # data=TokenSerializer(token).data,
            # data= jwttoken,
            status=status.HTTP_200_OK
        )


@ee.on('sendmail')
def sendmail(useremail, jwttoken):
    print(useremail)
    print(jwttoken)
    request = None
    from django.core.mail import EmailMessage

    url = 'http://127.0.0.1:8000' + \
        reverse('todo:verifytoken', args=[jwttoken])
    # http://127.0.0.1:8000/ToDoApp/verifytoken/'+jwttoken
    message = 'Dear User, </br> Please verify your email by clicking on the below link ' + \
        url + ' </br></br> Thank you, </br> Todo Team'
    email = EmailMessage('Subject', message, to=['ashtest1947@gmail.com'])
    email.send()

    print(url)
    return


class NoteList(generics.ListAPIView):

    serializer_class = NoteSerializer

    def get_queryset(self):
        id = self.request.META.get('HTTP_ID')
        print("this is id", id)
        user = User.objects.get(id=id)
        print(user)

        # collab = Collaborator.objects.filter(shareduser=id)

        queryset = Notes.objects.filter(
            owner=user).order_by('-last_modified')[:100]

        # print(queryset)
        queryset2 = Notes.objects.raw(
            'select * from "Todo_notes" where id in(select note_id from "Todo_collaborator" where shareduser_id= %s) ', [id])
        logger.warning("notes retrieved")
        if queryset == None:
            return queryset2
        print(queryset2)
        final_queryset = list(chain(queryset2, queryset))
        # serializer_class = NoteSerializer(Notes, context={"request": request})
       # print(final_queryset)

        if final_queryset:
            return final_queryset

    # serializer_class = NoteSerializer #(Notes, context={"request": request})


class CreateNote(generics.CreateAPIView):
    print("inside create")
    serializer_class = NoteSerializer


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer


class CreateProfile(generics.UpdateAPIView):
    print("inside create")
    serializer_class = NoteSerializer


class CreateListCollaborator(generics.ListCreateAPIView):
    serializer_class = CollaboratorSerializer

    def get_queryset(self):
        id = self.request.META.get('HTTP_NOTEID')
        print("this is id", id)
        note = Notes.objects.get(id=id)
        queryset = Collaborator.objects.filter(note=id)

        # serializer_class = NoteSerializer(Notes, context={"request": request})
        # print(queryset)

        if queryset:
            return queryset


class CollaboratorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer


class DeleteCollaborator(GenericAPIView):
    def get(self, request, *args, **kwargs):
        owner = kwargs['owner']
        note = kwargs['note']
        shareduser = kwargs['shareduser']
        print(owner, shareduser, note)
        collab = Collaborator.objects.get(
            owner=owner, note=note, shareduser=shareduser)
        collab.delete()
        logger.warning("deleted")
        return Response(status=status.HTTP_200_OK)


class GetUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetUserByUserName(generics.RetrieveAPIView):

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddImage(GenericAPIView):

    def post(self, request, *args, **kwargs):
        owner = request.data["owner"]
        profile = Profile.objects.get(owner=owner)
        print(request.data["file"])
        profile.photo = request.data["file"]
        profile.save()
        print(settings.MEDIA_ROOT)
        # data={
        #     'owner':profile.owner.id,
        #     'image':profile.image
        # }
        return Response(status=status.HTTP_200_OK)


class GetImage(GenericAPIView):

    def get(self, request, *args, **kwargs):
        owner = kwargs['owner']
        profile = Profile.objects.get(owner=owner)
        logger.warning("image retrieved successfully")

        data = {

            'image': str(profile.photo)
        }
        return Response(data=data, status=status.HTTP_200_OK)


class LabelCreate(GenericAPIView):
    def post(self, request, *args, **kwargs):
        label = request.data['label']
        id = self.request.META.get('HTTP_ID')
        print("this is id", id)
        user = User.objects.get(id=id)
        label = Labels.objects.create(owner=user, label=label)
        label.save()
        return Response(status=status.HTTP_201_CREATED)


class AddNoteToLabel(GenericAPIView):
    def post(self, request, *args, **kwargs):
        noteid = kwargs['note']
        note = Notes.objects.get(id=noteid)
        labelid = kwargs['label']
        label = Labels.objects.get(id=labelid)
        label.note.add(note)

        return Response(status=status.HTTP_201_CREATED)


class GetAllLabels(generics.ListCreateAPIView):
    serializer_class = LabelSerializer

    def get_queryset(self):

        id = self.request.META.get('HTTP_ID')
        print("this is id", id)
        user = User.objects.get(id=id)
        labels = Labels.objects.filter(owner=user)

        return labels


class GetAllLabelsFromNote(generics.ListCreateAPIView):
    serializer_class = LabelSerializer

    def get_queryset(self):

        id = self.request.META.get('HTTP_NOTEID')
        print("this is id", id)

        labels = Labels.objects.filter(note__id=id)

        return labels


class GetCollabFromNote(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):

        noteid = self.kwargs['note']
        list1 = []
        print(noteid)
        id = self.request.META.get('HTTP_ID')
        print("this is id", id)
        note = Notes.objects.get(id=noteid)

        collab = Collaborator.objects.filter(note=note).values('shareduser')

        print(collab.query)
        # print(collab)
        user = User.objects.all().filter(id__in=Subquery(collab))
        # #user=User.objects.raw('select  id,username from auth_user where auth_user.id in(select shareduser_id from "Todo_collaborator" where note_id=%s)',[noteid])
        print(user)
        print(user.query)
        return user

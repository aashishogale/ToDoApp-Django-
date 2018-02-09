from django.contrib.auth.models import User
from django.http import Http404, request, HttpResponseRedirect
from django.shortcuts import render, reverse, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from Todo.exceptions import ValueBlankError,TokenError
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

'''
    Class: UserRegisterView
    Param: generics.CreateAPIView
    Overview / Description: register the user

    def: create Function defination to create the user 
'''
class UserRegisterView(CreateAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
    
        try:
            
            serializer = self.get_serializer(data=request.data)

            #validate the user
            serializer.is_valid(raise_exception=True)

            #create the user
            self.perform_create(serializer)
            
            #creation of token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            user = serializer.instance
            payload = jwt_payload_handler(user)
            jwttoken = jwt_encode_handler(payload)
            
            #send mail
            ee.emit('sendmail', user.email, jwttoken)
            return Response(status=status.HTTP_201_CREATED)
        except Exception :
            data=serializer.errors

            
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)

'''
    Class: UserLoginView
    Param: GenericAPIView
    Overview / Description: login the user

    def: create Function defination to login the user 
'''
class UserLoginView(GenericAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            #get serialized user
            user = serializer.user

            #get json token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            jwttoken = jwt_encode_handler(payload)

            #set the cache
            cache = redis.StrictRedis(host='localhost', decode_responses=True)
            cache.set(jwttoken, user.username)
            logger.warning("logged in successfully")

            #set the data for response
            data = {
                "username": user.username,
                "id": user.id,
                "token": jwttoken

            }
            return Response(
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


'''
    Class:VerifyToken
    Param: GenericAPIView
    Overview / Description: verify the token from url

    def: get decode the token and check if user exists 
'''
class VerifyToken(GenericAPIView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        try:
          
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
            try:
                #get token from header
                payload = jwt_decode_handler(self.kwargs['token'])

                #check if token is present
                if payload==None:
                    raise ValueBlankError
                else:  

                    #get username from payload           
                    username = jwt_get_username_from_payload(payload)
                   
            except ValueBlankError:
                return redirect('http://127.0.0.1:8000/ToDoApp/#!/register')  

            #update the user
            User.objects.filter(username=username).update(is_active=True)
        
        
        except ObjectDoesNotExist:
                return redirect('http://127.0.0.1:8000/ToDoApp/#!/register')
        return redirect('http://127.0.0.1:8000/ToDoApp/')
    

        
'''
    Class:GenerateOTp
    Param: GenericAPIView
    Overview / Description: Generate the otp and send to user 

    def: post generate the  otp and send to the user
'''

class GenerateOTP(GenericAPIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print(request)
        try:
            data = request.data
            
            #get email from data
            useremail = data['email']
  
            #check if data and user is present
            if(data==None or useremail==None):
                raise ValueBlankError
        except ValueBlankError:
            data={
                "error":"bad request"
            }
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)
      
        try:
            #check if user with the email is present
            user = User.objects.get(email=useremail)
         
        except ObjectDoesNotExist:
            data={
                "error":"invalid user"
            }
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)

      
        #generate the random number
        randomno = randint(1000, 9999)

        #associate with the user email
        otp[str(randomno)] = user.email

        #generate jwt token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        jwttoken = jwt_encode_handler(payload)

        #send mail
        email = EmailMessage('Subject', str(randomno),
                                to=['ashtest1947@gmail.com'])
        email.send()
        return Response(
            # # data=TokenSerializer(token).data,
            data=jwttoken,
            status=status.HTTP_200_OK
        )


'''
    Class:CheckOTP
    Param: GenericAPIView
    Overview / Description: Check if otp matches to the user email 

    def: post check if otp matches the user
'''
class CheckOTP(GenericAPIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            #get randomno from request data
            randomno = data['otp']

            if(randomno==None or data==None):
                raise ValueBlankError
        except ValueBlankError:
            data={
                'error':' otp not found please try again'
            }
        try:

            #get useremail from otp 
            useremail = otp[str(randomno)]
        
    
            if(useremail==None):
                raise ValueBlankError
            else:
                #get user with email
                user = User.objects.get(email=useremail)

        except ObjectDoesNotExist:

            data={
                "error":"invalid user"
            }

            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)

        except ValueBlankError:

            data={

               "error":"invalid otp"
            }

            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)

        return Response(
        
            status=status.HTTP_200_OK
        )

'''
    Class:UserLogout
    Param: GenericAPIView
    Overview / Description: Logout the user

    def: get logout the user
'''

class UserLogoutView(GenericAPIView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        try:
            #get token from request header
            jwttoken = request.META.get('HTTP_TOKEN')

            if(jwttoken==None):
                raise ValueBlankError
            else:

                #deletefrom cache
                cache = redis.StrictRedis(host='localhost', decode_responses=True)
                cache.delete(jwttoken)

        except ValueBlankError:
            data={
                'error':'invalid token found'
            }
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)
        return Response( status=status.HTTP_200_OK )

'''
    Class:Change Password
    Param: GenericAPIView
    Overview / Description: Change password

    def: post Change password
'''
class ChangePassword(GenericAPIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            print(request.META.get('HTTP_TOKEN'))
            
            data = request.data

            #get password from request
            password = data['password']

            #check if password id present
            if(password==None):

                raise ValueBlankError 

        except ValueBlankError:
            data={
                'error':'invalid request'
            } 
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST) 

        try:  

            #perform jwt token decoding
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
            payload = jwt_decode_handler(request.META.get('HTTP_TOKEN'))

            #check if payload exists
            if(payload==None):

                raise TokenError
        except TokenError:

            data={
                'error':'token expired please try again'
            }

            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)

        try:    #get user from payload
            username = jwt_get_username_from_payload(payload)
            
            if(username==None):
                raise ValueBlankError
        except ValueBlankError:

            data={
                'error':'token expired please try again'
            }
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)

        try:
            #check if the user exists
            user = User.objects.get(username=username)

        except ObjectDoesNotExist:
            data={
                'error':'invalid user'
            }
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)

        #update the password  
        User.objects.filter(username=username).update(password=password)

        return Response(
         
            status=status.HTTP_200_OK
        )

'''
        def: send the mail
        filter: Default filter by logged in user.
'''
@ee.on('sendmail')
def sendmail(useremail, jwttoken):
   
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


'''
    Class: NoteList
    Param: generics.ListAPIView
    Overview / Description: Retrive the list of notes from the redis cache

    def: get_queryset Function defination to build the query 
'''
class NoteList(generics.ListAPIView):
    # Serializer Notes class 
    serializer_class = NoteSerializer

    '''
        def: Function to retrive the list of notes from the Notes model
        filter: Default filter by logged in user.
    '''
    def get_queryset(self):
        response_data = {}
        response_data['success'] = False
        response_data['message'] = "Something bad happened. Please try again." 
        response=[]

        # Retrive the logged in user id from the 
        user_id = self.request.META.get('HTTP_ID')

        # Get the logged in User Object
        try:
            user = User.objects.get( id = user_id)
        except ObjectDoesNotExist:

            logger.warning('Warning: No user_id:%d  %sn', user_id,  str(e))
            response_data['message'] = "Invalid user"
            response.append(response_data.copy())
            return response

        except Exception as e:

            logger.error('ERROR: %sn', str(e))
            response.append(response_data.copy())
            return response

        # Get the Notes corresponing to the user & order by latest
        try:
            queryset = Notes.objects.filter( owner = user ).order_by('-last_modified')[:100]
        except ObjectDoesNotExist:
            queryset = None

        # Get the Collabrated notes with the user
        try:
            queryset2 = Notes.objects.raw(
                'select * from "Todo_notes" where id in ( select note_id from "Todo_collaborator" where shareduser_id= %s) ', [user_id])
            logger.warning("notes retrieved")
        except ObjectDoesNotExist:
            queryset2 = None

        final_queryset = list(chain(queryset2, queryset))
        return final_queryset
        
        # if queryset2 and  queryset:
        #    
        #     response_data['data'] = final_queryset
        # else:
        #     response_data['data'] = []
        # return response_data


'''
    Class: create note
    Param: generics.CreateAPIView
    Overview / Description: Create the note

 
'''

class CreateNote(generics.CreateAPIView):
    print("inside create")
    serializer_class = NoteSerializer

'''
    Class: NoteDetail
    Param: generics.RetrieveUpdateDestroyAPIView
    Overview / Description: Create the note

 
'''
class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer


'''
    Class: CreateProfile
    Param: generics.UpdateAPIView
    Overview / Description: Create the Profile

 
'''
class CreateProfile(generics.UpdateAPIView):

    serializer_class = NoteSerializer

'''
    Class: CreateListCollaborator
    Param: generics.ListCreateAPIView
    Overview / Description: Create List Collaborator

 
'''
class CreateListCollaborator(generics.ListCreateAPIView):
    serializer_class = CollaboratorSerializer

    def get_queryset(self):
        try:
            id = self.request.META.get('HTTP_NOTEID')
            if(id==None):
                raise ValueBlankError
        except ValueBlankError:
            data={
                'data':'note does not exist'
            }
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)

        try:
            queryset = Collaborator.objects.filter(note=id)
        except ObjectDoesNotExist:
            return queryset

        
        return queryset

'''
    Class: CollaboratorDetail
    Param: generics.RetrieveUpdateDestroyAPIView
    Overview / Description: update and create  List Collaborator

 
'''
class CollaboratorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer

'''
    Class:Delete Colloborator
    Param: generics.ListCreateAPIView
    Overview / Description: Delete  Collaborator

 
'''
class DeleteCollaborator(GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            #get query parameters
            owner = kwargs['owner']
            note = kwargs['note']
            shareduser = kwargs['shareduser']

            #check if not none
            if(owner==None or note==None or shareduser==None):
                raise ValueBlankError
        except ValueBlankError:
            data={
                'error':'request error'

            }
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)
        try:
            #get collaborator
            collab = Collaborator.objects.get(
                owner=owner, note=note, shareduser=shareduser)
                
            collab.delete()
        except ObjectDoesNotExist:
            data={
                'error':'object not found'
            }
        logger.warning("deleted")
        return Response(status=status.HTTP_200_OK)

'''
    Class:GetUserView
    Param: generics.RetrieveAPIView
    Overview / Description: get all users

 
'''
class GetUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

'''
    Class:GetUserByUserName
    Param: generics.RetrieveAPIView
    Overview / Description: get all users

 
'''
class GetUserByUserName(generics.RetrieveAPIView):

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddImage(GenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            owner = request.data["owner"]
            if(owner==None):
                raise ValueBlankError
        except ValueBlankError:
                data={
                    'error':'bad request'
                }
                return Response(data=data,status=status.HTTP_400_BAD_REQUEST)
        try:
        
             profile = Profile.objects.get(owner=owner)
        except ObjectDoesNotExist:
                 data={
                     'error':'user does not exist'
                 }

  
        profile.photo = request.data["file"]
        profile.save()
        
      
        return Response(status=status.HTTP_200_OK)


class GetImage(GenericAPIView):

    def get(self, request, *args, **kwargs):
        try:
            owner = kwargs['owner']
        except ValueBlankError:
                data={
                    'error':'user does not exist'
                }
        try:
            profile = Profile.objects.get(owner=owner)
        except ObjectDoesNotExist:
            data={
                'error':'user does not exist'
            }
        logger.warning("image retrieved successfully")

        data = {

            'image': str(profile.photo)
        }
        return Response(data=data, status=status.HTTP_200_OK)


class LabelCreate(GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            label = request.data['label']

            id = self.request.META.get('HTTP_ID')
            if(id==None or label==None):
                raise ValueBlankError
        except ValueBlankError:
            data={
                'error':'bad request'
            }
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=id)
        except ObjectDoesNotExist:
            data={
                'error':'user does not exist'
            }
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

        id = self.kwargs['noteid']
        print("this is id", id)

        labels = Labels.objects.filter(notelabel__id=id)

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

class GetNotesFromLabel(generics.ListAPIView):
     serializer_class=NoteSerializer
     def get_queryset(self):
        labelid=self.kwargs["labelid"]
        labelednotes=Notes.objects.filter(label=labelid)
        return labelednotes
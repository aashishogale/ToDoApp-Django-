from django.contrib.auth.models import User
from django.http import Http404,request,HttpResponseRedirect
from django.shortcuts import render,reverse,render,redirect

from rest_framework import status, generics, serializers, viewsets
# from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.cache import never_cache
from Todo.serializers import ProfileSerializer,UserSerializer,UserLoginSerializer,TokenSerializer,NoteSerializer,CollaboratorSerializer
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework_jwt.settings import api_settings
from random import randint
from .models import Notes,Collaborator,Profile
from django.core.mail import EmailMessage
from django.core.cache import cache
from pyee import EventEmitter
import asyncio
from functools import wraps
import redis
from django.db.models import Q
from itertools import chain
# from rest_framework import 


# Create your views here.
otp={}
ee = EventEmitter()



class UserRegisterView(CreateAPIView):

   
    
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    @csrf_exempt
    def create(self, request, *args, **kwargs):
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

       
        ee.emit('sendmail',user.email,jwttoken)
        return Response(status=status.HTTP_201_CREATED)
       

def startlogin(request):
     return render(request,'Todo/index.html')     

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
        
            cache=redis.StrictRedis(host='localhost',decode_responses=True)
            cache.set(jwttoken,user.username)
           
            data={
                "username":user.username,
                "id":user.id,
                "token":jwttoken

            }
            return Response(
                # data=TokenSerializer(token).data,
                data=data,
                status=status.HTTP_200_OK,
                
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @csrf_exempt
    def delete(self,request,format=None):

        logout(request)
        return Response(status=status.HTTP_200_OK)



class VerifyToken(GenericAPIView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        
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
    

        #print(request.get_absolute_url(self))
       
class GenerateOTP(GenericAPIView):
     @csrf_exempt
     def post(self, request, *args, **kwargs):
        data=request.data
        print(data)
        useremail=data['email']
        print(useremail)
        user=User.objects.get(email=useremail)
        users=User.objects.all()
        if user in users:
        
            randomno=randint(1000, 9999)
           
            otp[str(randomno)]=user.email
            print(otp[str(randomno)])
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            jwttoken = jwt_encode_handler(payload)
            email = EmailMessage('Subject', str(randomno), to=['ashtest1947@gmail.com'])
            email.send()
            return Response(
                # # data=TokenSerializer(token).data,
                data= jwttoken,
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
        data=request.data
        print(data)
        randomno=data['otp']
        print(randomno)
        print(otp)
        useremail=otp[str(randomno)]
        print(useremail)
        user=User.objects.get(email=useremail)
        users=User.objects.all()
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
        jwttoken=request.META.get('HTTP_TOKEN')
  
        cache=redis.StrictRedis(host='localhost',decode_responses=True)
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
        data=request.data
        password=data['password']
        print(password)
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
        payload = jwt_decode_handler(request.META.get('HTTP_TOKEN'))
        print(payload)
        username = jwt_get_username_from_payload(payload)
        print(username)
        users=User.objects.all()
        user=User.objects.get(username=username)
        # if user in users:
        User.objects.filter(username=username).update(password=password)
        return Response(
                # # data=TokenSerializer(token).data,
                # data= jwttoken,
                status=status.HTTP_200_OK
            )
        



@ee.on('sendmail')
def sendmail(useremail,jwttoken):
    print(useremail)
    print(jwttoken)
    request = None
    from django.core.mail import EmailMessage
  
    url = 'http://127.0.0.1:8000' + reverse('todo:verifytoken', args=[jwttoken]) 
    #http://127.0.0.1:8000/ToDoApp/verifytoken/'+jwttoken
    message = 'Dear User, </br> Please verify your email by clicking on the below link '+ url + ' </br></br> Thank you, </br> Todo Team'
    email = EmailMessage('Subject', message, to=['ashtest1947@gmail.com'])
    email.send()
    import time
    time.sleep(50)
    print(url)
    return


class NoteList(generics.ListAPIView):
 
    serializer_class = NoteSerializer
    queryset=Notes.objects.all()
    def get_queryset(self):
        id=self.request.META.get('HTTP_ID')
        print("this is id",id)
        user=User.objects.get(id=id)
        print(user)
        collab=Collaborator.objects.filter(shareduser=id)
        #print(collab)
        queryset=Notes.objects.filter(owner=user).order_by('-last_modified')[:100]
       # print(queryset)
        queryset2=Notes.objects.filter(id__in=collab)
        #print(queryset2)  
        final_queryset=list(chain(queryset2,queryset))
        # serializer_class = NoteSerializer(Notes, context={"request": request})
        #print(queryset)
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
        id=self.request.META.get('HTTP_NOTEID')
        print("this is id",id)
        note=Notes.objects.get(id=id)
        queryset=Collaborator.objects.filter(note=note)
      
      
        # serializer_class = NoteSerializer(Notes, context={"request": request})
        #print(queryset)
        if queryset:
          return queryset

class CollaboratorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer



class DeleteCollaborator(GenericAPIView):
        def get(self, request, *args, **kwargs):
            owner=kwargs['owner']
            note=kwargs['note']
            shareduser=kwargs['shareduser']
            print(owner,shareduser,note)
            collab=Collaborator.objects.get(owner=owner,note=note,shareduser=shareduser)
            collab.delete()
            return Response(status=status.HTTP_200_OK)

class GetUserView(generics.RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class GetUserByUserName(generics.RetrieveAPIView):

    lookup_field='username'
    queryset=User.objects.all()
    serializer_class=UserSerializer


class AddImage(GenericAPIView):

        def post(self, request, *args, **kwargs):
            owner=request.data["owner"]
            profile=Profile.objects.get(owner=owner)
            print(request.data["file"])
            profile.photo=request.data["file"]
            profile.save()
         
            # data={
            #     'owner':profile.owner.id,
            #     'image':profile.image
            # }
            return Response(status=status.HTTP_200_OK)

class getImage(generics.RetrieveAPIView):
    lookup_field="owner"
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
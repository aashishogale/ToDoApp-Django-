from django.contrib.auth.models import User
from django.http import Http404,request,HttpResponseRedirect
from django.shortcuts import render,reverse,render,redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from Todo.serializers import UserSerializer,UserLoginSerializer,TokenSerializer
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework_jwt.settings import api_settings

# Create your views here.

class UserRegisterView(CreateAPIView):

   
    
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
       # token, created = Token.objects.get_or_create(user=user)
       # data = serializer.data
        #data["token"] = token.key

        #headers = self.get_success_headers(serializer.data)
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
            return Response(
                # data=TokenSerializer(token).data,
                data= jwttoken,
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

class HomeView(GenericAPIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
      print(request.META.get('HTTP_TOKEN'))
    #   token=Token.objects.get(key=request.META.get('HTTP_TOKEN'))  
      jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
      jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
      payload = jwt_decode_handler(request.META.get('HTTP_TOKEN'))
      print(payload)
      username = jwt_get_username_from_payload(payload)
      print(username)
    #   print(token.user_id)
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
       
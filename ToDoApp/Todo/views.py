from django.contrib.auth.models import User
from django.http import Http404,request,HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from Todo.serializers import UserSerializer,UserLoginSerializer,TokenSerializer
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token


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
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
       

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
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
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
<<<<<<< HEAD
   
=======
>>>>>>> djbAuth
    @csrf_exempt
    def post(self, request, *args, **kwargs):
      print(request.META.get('HTTP_TOKEN'))
      token=Token.objects.get(key=request.META.get('HTTP_TOKEN'))  
      print(token.user_id)
      return Response(status=status.HTTP_200_OK)

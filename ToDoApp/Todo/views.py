from django.contrib.auth.models import User
from django.http import Http404,request
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from Todo.serializers import UserSerializer
from django.utils.decorators import method_decorator


# Create your views here.

class UserRegisterView(APIView):
     @csrf_exempt
     def post(self, request, format=None):
        
        serializer = UserSerializer(data=request.data)
             
        if serializer.is_valid():
          
            serializer.save()
         
            return Response(serializer.data, status=status.HTTP_201_CREATED)
       
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
       
       
     
    


class UserLoginView(APIView):
  
    @csrf_exempt
    def post(self,request,format=None):
     
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            print ('you are here')
            login(request,user)
            return Response(request.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    def delete(self,request,format=None):

        logout(request)
        return Response(status=status.HTTP_200_OK)


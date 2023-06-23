from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .utils import get_tokens_for_user
from django.shortcuts import get_object_or_404

from .serializers import RegistrationSerializer, PasswordChangeSerializer
# Create your views here.
from . models import *
from .serializers import *

@api_view(['GET'])
def display_users(request):
    # permission_classes = [IsAuthenticated, ]
    data=MyUser.objects.all()                          
    serilaizer=UserSerializer(data,many=True)    
    return Response(serilaizer.data)

@api_view(['GET'])
def display_user(request,id):
    data=get_object_or_404(MyUser,id=id)
    serializer=UserSerializer(data).data        
    return Response(serializer)

@api_view(['PUT'])
def update_user(request,id):
    data=get_object_or_404(MyUser,id=id)
    serializer=UserSerializer(data,data=request.data)  
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status.HTTP_200_OK)
    return Response(serializer._errors,status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    permission_classes = [AllowAny, ]
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
class LoginView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

      
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


      
class ChangePasswordView(APIView):
    # permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) #Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
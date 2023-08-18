from datetime import timedelta
import datetime
import jwt
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from authentication.models import User
from authentication.serializers import UserSerializer
from django.core.files.storage import default_storage

import json
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import authentication, permissions
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
import requests

# from authentication.tokens import create_jwt_pair_for_user
from config.settings import SECRET_KEY
# from rest_framework.permissions import IsAuthenticated

# Create your views here.

class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer
    # permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            # user = serializer.save()
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')
            user = User.objects.create_user(username=username, password=password, email=email)
            # refresh = AccessToken.for_user(user)
            user_info = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'isAdmin': user.is_superuser,
            'created_at': user.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }
            # tokens = create_jwt_pair_for_user(user)

            # Gửi yêu cầu tạo người dùng mới tới User Service
            user_service_url = 'http://localhost:8002/create_user/'
            user_data = {
                'username': user.username,
                'email': user.email,
                'phone': request.data.get('phone'),
            }
            response = requests.post(user_service_url, json=user_data)

            if response.status_code == 201:
                secret_key = SECRET_KEY
                token = jwt.encode({'user_info': user_info, 'exp': datetime.datetime.utcnow() + timedelta(days=1)}, secret_key, algorithm='HS256')

                response_data = {
                    "message": "User Created Successfully",
                    "data": serializer.data,
                    "token": token
                }

                return Response(data=response_data, status=status.HTTP_201_CREATED)
            else:
                # Xử lý lỗi tạo người dùng bên User Service
                user.delete()  # Xóa người dùng đã tạo trong Auth Service
                return Response(data={"error": "Failed to create user in User Service"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # permission_classes = []

    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            user_info = {
            'id': user.id,
            'username': username,
            'email': user.email,
            'isAdmin': user.is_superuser,
            'created_at': user.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }
            # tokens = create_jwt_pair_for_user(user)
            secret_key = SECRET_KEY
            token = jwt.encode({'user_info': user_info, 'exp': datetime.datetime.utcnow() + timedelta(days=1)}, secret_key, algorithm='HS256')

            response = {"message": "Login Successfull", "user": user_info, "tokens": token}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)

class userApi(APIView):
    
    # authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request: Request):
        users = list(User.objects.all().values('email', 'id', 'username'))
        return Response(users)
import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from user.models import User
from user.serializers import UserSerializer
from django.core.files.storage import default_storage

import json
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator

from .decorators import jwt_auth_required

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

class userApi(APIView):
    @method_decorator(jwt_auth_required)
    def get(self, request: Request):
        user_info = User.objects.get(id=request.user_info['id'])
        response = {
            'id': user_info.id,
            'username': user_info.username,
            'email': user_info.email,
            'phone': user_info.phone,
            'full_name': user_info.full_name,
            'avatar': user_info.avatar,
            'points': user_info.points,
            'created_at': user_info.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': user_info.updated_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'about': user_info.about,
        }
        return JsonResponse(response, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data

        # Kiểm tra xem người dùng đã tồn tại chưa
        id = data.get('id')
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        is_superuser = data.get('is_superuser')

        if User.objects.filter(username=username).exists():
            return Response(data={"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User(id=id, username=username, email=email, phone=phone, is_superuser=is_superuser)
        user.save()

        return Response(data={"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    
    @method_decorator(jwt_auth_required)
    def put(self, request):
        data = request.data
        user_info = request.user_info
        if request.query_params.get("id"):
            user_id = request.query_params.get("id")
            if user_info["isAdmin"] == True:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "You are not Administator."}, status=status.HTTP_403_FORBIDDEN)
        else:
            try:
                user = User.objects.get(id=user_info['id'])
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if data.get('username') is not None:
            if user_info["isAdmin"] == True:
                user.username = data.get('username')
            else:
                return Response({"message": "You are not Administator."}, status=status.HTTP_403_FORBIDDEN)
           
        if data.get('email') is not None:
            email_exists = User.objects.filter(email=data.get('email')).exists()
            if email_exists:
                return Response(data={"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.email = data.get('email')
        if data.get('phone') is not None:
            user.phone = data.get('phone')
        if data.get('full_name') is not None:
            user.full_name = data.get('full_name')
        if data.get('avatar') is not None:
            user.avatar = data.get('avatar')
        if data.get('role') is not None:
            if user_info["isAdmin"] == True:
                user.role = data.get('role')
            else:
                return Response({"message": "You are not Administator."}, status=403)
        if data.get('points') is not None:
            user.points = data.get('points')

        user.updated_date = datetime.datetime.now()
        user.save()
        return Response(data={"message": "User updated successfully"}, status=status.HTTP_200_OK)
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

# @csrf_exempt
# def userApi(request, id=0):
#     if request.method == 'GET':
#         users = User.objects.all()
#         users_serializer = UserSerializer(users, many=True)
#         return JsonResponse(users_serializer.data, safe=False)
#     elif request.method == 'POST':
#         users_data = JSONParser().parse(request)
#         users_serializer = UserSerializer(data=users_data)
#         if users_serializer.is_valid():
#             users_serializer.save()
#             return JsonResponse("Added Successfully!!", safe=False)
#         return JsonResponse("Failed to Add.", safe=False)
#     elif request.method == 'PUT':
#         users_data = JSONParser().parse(request)
#         users = User.objects.get(User_ID=users_data['User_ID'])
#         users_serializer = UserSerializer(users, data=users_data)
#         if users_serializer.is_valid():
#             users_serializer.save()
#             return JsonResponse("Updated Successfully!!", safe=False)
#         return JsonResponse("Failed to Update.", safe=False)
#     elif request.method == 'DELETE':
#         users = User.objects.get(User_ID=id)
#         users.delete()
#         return JsonResponse("Deleted Succeffully!!", safe=False)

class userApi(APIView):
    # def get(self, request: Request):
    #     users = list(User.objects.all().values('email', 'id', 'username'))
    #     return Response(users)
    @method_decorator(jwt_auth_required)
    def get(self, request: Request):
        user_info = request.user_info
        return Response(user_info)
    
@api_view(['POST'])
def create_user(request):
    data = request.data

    # Kiểm tra xem người dùng đã tồn tại chưa
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')

    if User.objects.filter(username=username).exists():
        return Response(data={"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User(username=username, email=email, phone=phone)
    user.save()

    return Response(data={"message": "User created successfully"}, status=status.HTTP_201_CREATED)
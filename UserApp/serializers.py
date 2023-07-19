from rest_framework import serializers
from UserApp.models import User
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('User_ID', 'User_Name')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "phone"]

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        
        password = validated_data.pop("password")
        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        Token.objects.create(user=user)

        return user
    
# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password', 'full_name', 'avatar', 'email', 'phone', 'role')
        
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#             full_name=validated_data['full_name'],
#             avatar=validated_data['avatar'],
#             email=validated_data['email'],
#             phone=validated_data['phone'],
#             role=validated_data['role'],
#         )
#         return user
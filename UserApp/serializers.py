from rest_framework import serializers
from UserApp.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('User_ID', 'User_Name')
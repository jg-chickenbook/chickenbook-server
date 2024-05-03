from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    
    is_visible = serializers.BooleanField(required=False)
    
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'email', 'is_visible']
        

class UserPublicSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    
    class Meta(object):
        model = UserProfile 
        fields = ['is_visible', 'user_id', 'username', 'email']
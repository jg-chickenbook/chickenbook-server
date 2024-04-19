from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    
    is_visible = serializers.BooleanField(source='profile.is_visible')
    
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'email', 'is_visible']
        

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['username', 'email']
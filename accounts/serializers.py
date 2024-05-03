from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile, Skills, Projects

class UserSerializer(serializers.ModelSerializer):
    
    is_visible = serializers.BooleanField(required=False)
    
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'email', 'is_visible']


class SkillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Skills
        fields = ['id', 'name']        

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'name', 'link']

class UserPublicSerializer(serializers.ModelSerializer):
    
    # username = serializers.CharField(source='user.username')
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    email = serializers.CharField(source='user.email')

    
    class Meta(object):
        model = UserProfile 
        fields = ['user_id', 'email', 'status', 'name', 'headline', 'phone_number', 'email', 'about', 'skills', 'projects']
        
        
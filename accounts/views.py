from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from accounts.serializers import UserSerializer, UserPublicSerializer, SkillSerializer, ProjectSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from accounts.models import UserProfile, Skills, Projects
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def login(request: Request) -> Response:
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)  # This method handles user verification
    print(user)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        # Exclude sensitive data from the response
        data = serializer.data
        if 'password' in data:
            del data['password']  # Ensure 'password' field is not included
        return Response({"token": token.key, "user": data}, status=status.HTTP_200_OK)
    else:
        # Providing a more generic error message for security
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def register(request: Request) -> Response:
    username = request.data.get('username', '')
    email = request.data.get('email', '')
    password = request.data.get('password', '')

    # Check if user or email already exists
    if User.objects.filter(username=username).exists():
        return Response({"detail": f"User with username {username} already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"detail": f"User with email {email} already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # Validate password
    try:
        validate_password(password)
    except ValidationError as e:
        return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        user_data = serializer.data
        if 'password' in user_data:
            del user_data['password']
        return Response({"token": token.key, "user": user_data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request: Request) -> Response:
    """_summary_

    Args:
        request (POST): _description_

    Token Deletion
    Returns:
        json: logout msg
    """
    # Delete the token to log the user out
    request.user.auth_token.delete()
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_user_public_profile(request: Request, user_id: int) -> Response:
    try:
        user = UserProfile.objects.get(user_id=user_id, is_visible=True)
        serializer = UserPublicSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def get_logged_user_profile(request: Request, username: str) -> Response:
#     if request.user.username != username:
#         # If the requesting user is not the same as the username in the URL, return unauthorized
#         return Response({"detail": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
#     try:
#         user = User.objects.get(username=username)
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except User.DoesNotExist:
#         # User not found
#         return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_logged_user_profile(request, username):
    if request.user.username != username:
        return Response({"detail": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
    try:
        user_profile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserPublicSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = UserPublicSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    


@api_view(['GET'])
def get_visible_users(request: Request) -> Response:
    users = UserProfile.objects.filter(is_visible=True)
    if users:
        serializer = UserPublicSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"detail": "No users found"})

# SKILLS

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_skill(request: Request) -> Response:
    serializer = SkillSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user_profile=request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def skill_detail(request: Request, pk: int) -> Response:
    try:
        skill = Skills.objects.get(pk=pk, user_profile=request.user.profile)
    except Skills.DoesNotExist:
        return Response({'detail': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SkillSerializer(skill)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        skill.delete()
        return Response({'detail': 'Skill deleted'}, status=status.HTTP_204_NO_CONTENT)
    
# PROJECTS

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_project(request: Request) -> Response:
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user_profile=request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def project_detail(request: Request, pk: int) -> Response:
    try:
        project = Projects.objects.get(pk=pk, user_profile=request.user.profile)
    except Projects.DoesNotExist:
        return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        project.delete()
        return Response({'detail': 'Project deleted'}, status=status.HTTP_204_NO_CONTENT)


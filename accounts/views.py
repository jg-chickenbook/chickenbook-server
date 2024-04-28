from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from accounts.serializers import UserSerializer, UserPublicSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from accounts.models import UserProfile
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

#Make sure the tokens works also template for authentificated user 
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request: Request):
    """_summary_

    Args:
        request (GET): _description_

    Function return passed msg if user is logged in !
    Returns:
        json: validation msg
    """
    print(request.user)
    return Response("passed for {}".format(request.user.username))

@api_view(['GET'])
def get_user_public_profile(request: Request, username: str) -> Response:
    try:
        user = UserProfile.objects.get(username=username, is_visible=True)
        serializer = UserPublicSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_logged_user_profile(request, username):
    if request.user.username != username:
        # If the requesting user is not the same as the username in the URL, return unauthorized
        return Response({"detail": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        # User not found
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_visible_users(request: Request) -> Response:
    users = UserProfile.objects.filter(is_visible=True)
    if users:
        serializer = UserPublicSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"detail": "No users found"})
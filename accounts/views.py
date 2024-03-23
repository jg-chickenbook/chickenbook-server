from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
# from django.shortcuts import get_object_or_404

# imports for make sure the tokens works
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# @api_view(['POST'])
# def login(request):
#     """_summary_

#     Args:
#         request (POST): _description_

#     Returns:
#         json: with auth(token) and user data  
#     """
#     user = get_object_or_404(User, username=request.data['username'])
#     if not user.check_password(request.data['password']):
#         return Response({"detail": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
#     token, created = Token.objects.get_or_create(user=user)
#     serializer = UserSerializer(instance=user)
#     # tady se mi vrací v Response celý objekt user to asi není to pravé protože tam je i zahashované heslo
#     # return Response({"token": token.key, "user": serializer.data})
#     # spíš by zde mělo být něco jako je toto
#     return Response({"token": token.key, "user": serializer.data.get('username')})

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)  # This method handles user verification
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
def register(request):
    """_summary_

    Args:
        request (POST): _description_

    Returns:
        json: if serializer is valid returns token and user info 
    """
    
    username = request.data.get('username', '')
    email = request.data.get('email', '')
    
    if User.objects.filter(username=username).exists():
        return Response({"error": f"User with {username} already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({"error": f"User with {email} already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
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
def test_token(request):
    """_summary_

    Args:
        request (GET): _description_

    Function return passed msg if user is logged in !
    Returns:
        json: validation msg
    """
    print(request.user)
    return Response("passed for {}".format(request.user.username))
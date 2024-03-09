from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User 
from django.shortcuts import get_object_or_404

# imports for make sure the tokens works
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    # tady se mi vrací v Response celý objekt user to asi není to pravé protože tam je i zahashované heslo
    # return Response({"token": token.key, "user": serializer.data})
    # spíš by zde mělo být něco jako je toto
    return Response({"token": token.key, "user": serializer.data.get('username')})

@api_view(['POST'])
def register(request):
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
    # Delete the token to log the user out
    request.user.auth_token.delete()
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)

#Make sure the tokens works also template for authentificated user 
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    print(request.user)
    return Response("passed for {}".format(request.user.username))
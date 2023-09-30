from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, logout, login

from users.serializers import UserSerializer


@api_view(['POST'])
def UserRegistrationView(request):
    if request.user.is_authenticated:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "you need to logout first"})
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(status=status.HTTP_201_CREATED, data={"message": "You successfully registered!"})

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "You are already logged in!"})
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(email=email, password=password, username=username)

        if user:
            login(request, user)
            return Response(data={"message": "You successfully logged in"},
                            status=status.HTTP_200_OK)

        return Response({'error': "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)

        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': "You successfully logged out."})

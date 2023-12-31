from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, logout, login

from users.serializers import RegisterSerializer


def is_email_existing(email):
    return User.objects.filter(email=email).exists()


class UserRegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        email = request.data.get('email')

        if request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "you need to logout first"})

        serializer = self.serializer_class(data=request.data)

        if is_email_existing(email):
            return Response(data={"error": "This email already exists, try with another one."},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={"message": "You successfully registered!"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

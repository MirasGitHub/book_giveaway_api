from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=150, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "password", 'email']

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data['email']

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=150, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']


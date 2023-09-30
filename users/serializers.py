from rest_framework import serializers
from django.contrib.auth.models import User


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
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

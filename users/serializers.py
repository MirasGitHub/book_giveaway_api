from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data['username']
        password = validated_data['password']

        user = User.objects.create_user(email=email, username=username, password=password)
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

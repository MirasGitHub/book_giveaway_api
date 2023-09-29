from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Author, Genre, Condition


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')
    book_genre = serializers.ReadOnlyField(source='genre.name')
    book_condition = serializers.ReadOnlyField(source='condition.name')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    is_offered = serializers.BooleanField()
    interested_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'location', 'is_available', 'author', 'author_name', 'genre', 'book_genre',
                  'condition', 'book_condition', 'is_offered', 'interested_users', 'owner_username', 'author', 'title', 'location', 'book_condition', 'is_available']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation.pop('author')
        representation.pop('genre')
        representation.pop('condition')

        return representation

    def create(self, validated_data):
        validated_data.pop('author_name', None)
        validated_data.pop('book_genre', None)
        validated_data.pop('book_condition', None)
        validated_data.pop('owner_username', None)

        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)




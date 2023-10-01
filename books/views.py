from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import BookFilter
from rest_framework.filters import SearchFilter
from .models import Author, Genre, Condition, Book
from .permissions import BasePermissionViewSet
from .serializers import AuthorSerializer, GenreSerializer, ConditionSerializer, BookSerializer


class AuthorViewSet(BasePermissionViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreViewSet(BasePermissionViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ConditionViewSet(BasePermissionViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer


class BookViewSet(BasePermissionViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.OrderingFilter, SearchFilter)
    filterset_class = BookFilter
    ordering_fields = ['author', 'id', 'condition', 'title', 'location', 'owner', 'genre']
    search_fields = ['location', 'title', 'author__name', "condition__name", 'genre__name', 'is_available', 'owner__username']

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Book.objects.filter(Q(is_available=True) | Q(owner=user))

        return Book.objects.filter(is_available=True)

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        if book.owner != request.user:
            return Response(
                {"detail": "You do not have permission to perform this action, as you are not the owner of this book!"},
                status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def perform_book_deletion(self, request, book):
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        if book.owner != request.user:
            return Response({"error": "You do not have permission to perform this action, as you're not the owner of this book!"},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_book_deletion(request, book)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='offer-book')
    def offer_book(self, request, pk=None):
        book = self.get_object()
        if book.owner != request.user:
            return Response({'message': "You can not offer as you are not the owner of this book!"},
                            status=status.HTTP_403_FORBIDDEN)

        book.is_offered = True
        book.save()
        return Response({'message': "Book offered successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='take-book')
    def take_book(self, request, pk=None):
        book = self.get_object()

        if book.owner == request.user:
            return Response({'message': 'You are the owner of this book. Owners cannot express interest.'},
                            status=status.HTTP_403_FORBIDDEN)

        if not book.is_offered:
            return Response({'message': "Currently, the book is not offered for free"})

        if request.user.is_authenticated:
            book.interested_users.add(request.user)
            book.save()
            return Response({'message': 'You have expressed interest in taking this book.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Authentication is required to take a book.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], url_path='choose-recipient')
    def choose_recipient(self, request, pk=None):
        book = self.get_object()

        if book.owner != request.user:
            return Response({'message': 'You are not the owner of this book.'}, status=status.HTTP_403_FORBIDDEN)

        if not book.is_offered:
            return Response({'message': 'This book is not offered for free.'}, status=status.HTTP_400_BAD_REQUEST)

        interested_users = book.interested_users.all()

        if not interested_users.exists():
            return Response({'message': 'No interested users for this book.'}, status=status.HTTP_400_BAD_REQUEST)

        recipient_user_id = request.data.get('recipient_user_id')

        try:
            recipient = interested_users.get(id=recipient_user_id)
        except User.DoesNotExist:
            return Response({'message': 'Invalid recipient user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        book.interested_users.set([recipient])
        book.owner = recipient
        book.is_offered = False
        book.save()

        return Response({'message': f'Recipient chosen: {recipient.username}'}, status=status.HTTP_200_OK)


class UserBookViewSet(BasePermissionViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Please register or log in.'}, status=status.HTTP_403_FORBIDDEN)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(owner=user)


class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = self.serializer_class(instance=book)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=book, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('pk')
        book = Book.objects.get(pk=book_id)

        file_serializer = BookSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(book=book)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

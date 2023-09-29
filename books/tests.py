from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Book, Author, Condition, Genre


class AuthorViewSetTests(APITestCase):
    def test_get_author_list(self):
        url = reverse('authors-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GenreViewSetTests(APITestCase):
    def test_get_genre_list(self):
        url = reverse('genre-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ConditionViewSetTests(APITestCase):
    def test_get_condition_list(self):
        url = reverse('condition-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserBookViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get_user_book_list(self):
        url = reverse('user-books-list')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookDetailTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password="testpassword")
        self.client.login(username='testuser', password='testpassword')
        self.author = Author.objects.create(name='Test Author')
        self.condition = Condition.objects.create(name='Test Condition')
        self.genre = Genre.objects.create(name='Test Condition')
        self.book = Book.objects.create(title='Test Title', author=self.author, condition=self.condition, genre=self.genre,  owner=self.user, location='Some Location', is_available=True, is_offered=False)

    def test_get_all_books(self):
        url = reverse('books-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_book_detail(self):
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        url = reverse('books-list')
        data = {
            'title': 'New Book',
            'author': self.author.pk,
            'condition': self.condition.pk,
            'genre': self.genre.pk,
            'owner': self.user.pk,
            'is_available': True,
            'is_offered': False,
            'location': 'Test location'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        data = {
            'title': 'Updated Book Title'
        }
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_206_PARTIAL_CONTENT)

    def test_delete_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)





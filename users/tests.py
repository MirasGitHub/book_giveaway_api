from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testUser', password='testPassword')

    def test_user_registration_view(self):
        url = reverse('user-register')
        data = {'username': 'testuser2', 'password': 'testpassword2'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_registration_authenticated_view(self):
        User.objects.create_user(username='existinguser', password='password')
        data = {'username': 'existinguser', 'password': 'password'}
        url = reverse('user-register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_view(self):
        url = reverse('user-login')
        data = {'username': 'testUser', 'password': 'testPassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout_view(self):
        self.client.login(username='testUser', password='testPassword')
        url = reverse('user-logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

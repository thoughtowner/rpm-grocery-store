from django.contrib.auth.models import User
from django.test import TestCase
from django.test import client as test_client
from rest_framework import status


class TestRegistration(TestCase):
    _url = '/register/'
    _valid_creds = {
        'username': 'user',
        'password1': 'some_kind_of_password_running_in_the_test',
        'password2': 'some_kind_of_password_running_in_the_test',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@mail.com',
    }

    def setUp(self):
        self.client = test_client.Client()

    def test_invalid(self):
        invalid_creds = self._valid_creds.copy()
        invalid_creds['password1'] = 'wrong_password'
        self.client.post(self._url, invalid_creds)
        self.assertEqual(len(User.objects.filter(username='user')), 0)

    def test_valid(self):
        self.client.post(self._url, self._valid_creds)
        self.assertEqual(len(User.objects.filter(username='user')), 1)

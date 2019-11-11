import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

client = Client()


class SignInTest(TestCase):
    def setUp(self):
        self.valid_request = {
            'user': {'username': 'alex',
                     'password': '1111',
                     'password_confirm': '1111',
                     'first_name': 'Alexandr',
                     'last_name': 'Ivanov',
                     'email': 'alex@gmail.com'},
            'birthday': '1998-08-08'
        }

        self.password_confirm_not_match_request = {
            'user': {'username': 'alex',
                     'password': '1111',
                     'password_confirm': '2222',
                     'first_name': 'Alexandr',
                     'last_name': 'Ivanov',
                     'email': 'alex@gmail.com'},
            'birthday': '1998-08-08'
        }

        self.not_existence_email_request = {
            'user': {'username': 'alex',
                     'password': '1111',
                     'password_confirm': '1111',
                     'first_name': 'Alexandr',
                     'last_name': 'Ivanov',
                     'email': 'alex@ukfr.net'},
            'birthday': '1998-08-08'
        }

    def test_valid_registration(self):
        response = client.post(reverse('register'),
                               data=json.dumps(self.valid_request),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_password_confirm_not_match(self):
        response = client.post(reverse('register'),
                               data=json.dumps(self.password_confirm_not_match_request),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertAlmostEqual(response.data['password'], 'Password must match.')

    def test_register_not_existence_email(self):
        response = client.post(reverse('register'),
                               data=json.dumps(self.not_existence_email_request),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertAlmostEqual(response.data['email'], 'Email does not exist.')


class CreatePostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alex', password='1111')
        self.user_data = {
            'username': 'alex',
            'password': '1111'
        }
        self.valid_post_request = {
            'title': 'Hobbit',
            'description': 'Movie',
        }

    def test_successful_create_post(self):
        response = client.post(reverse('token_obtain_pair'),
                               data=self.user_data,
                               content_type='application/json')
        access_token = response.data['access']
        response = client.post(reverse('create_post'),
                               data=self.valid_post_request,
                               HTTP_AUTHORIZATION='Bearer ' + access_token,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

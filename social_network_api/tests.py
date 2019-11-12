import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from social_network_api.models import Post

client = Client()


def get_access_token(user_data):
    response = client.post(reverse('token_obtain_pair'),
                           data=user_data,
                           content_type='application/json')
    access_token = response.data['access']
    if response.status_code == status.HTTP_200_OK:
        return access_token
    else:
        return None


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


class LogInTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alex', password='1111')
        self.valid_user_data = {
            'username': 'alex',
            'password': '1111'
        }
        self.not_exist_user_data = {
            'username': 'ivan',
            'password': '1111'
        }

    def test_success_login(self):
        response = client.post(reverse('token_obtain_pair'),
                               data=self.valid_user_data,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_not_existence_user(self):
        response = client.post(reverse('token_obtain_pair'),
                               data=self.not_exist_user_data,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertAlmostEqual(response.data['detail'], 'No active account found with the given credentials')


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
        self.post_without_title_request = {
            'description': 'Movie',
        }

    def test_successful_create_post(self):
        access_token = get_access_token(self.user_data)
        response = client.post(reverse('create_post'),
                               data=self.valid_post_request,
                               HTTP_AUTHORIZATION='Bearer ' + access_token,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_without_auth(self):
        response = client.post(reverse('create_post'),
                               data=self.valid_post_request,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_without_title(self):
        access_token = get_access_token(self.user_data)
        response = client.post(reverse('create_post'),
                               data=self.post_without_title_request,
                               HTTP_AUTHORIZATION='Bearer ' + access_token,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertAlmostEqual(response.data['title'][0], 'This field is required.')


class LikePostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alex', password='1111')
        self.post = Post.objects.create(title='Hobbit', description='Movie', created_by=self.user)
        self.user_data = {
            'username': 'alex',
            'password': '1111'
        }

    def test_user_like_post(self):
        access_token = get_access_token(self.user_data)
        pk = self.post.id
        response = client.put(reverse('like_post', kwargs={'pk': pk}),
                              HTTP_AUTHORIZATION='Bearer ' + access_token,
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['success'],
                               'Post {} like by {}'.format(self.post.title, self.user.username))

    def test_user_unlike_post(self):
        self.post.users_likes.add(self.user)  # user already like post
        access_token = get_access_token(self.user_data)
        pk = self.post.id
        response = client.put(reverse('like_post', kwargs={'pk': pk}),
                              HTTP_AUTHORIZATION='Bearer ' + access_token,
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['success'],
                               'Post {} unlike by {}'.format(self.post.title, self.user.username))

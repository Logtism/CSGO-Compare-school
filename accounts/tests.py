from django.test import TestCase, Client
from django.conf import settings
from firebrick.tests import ResolveUrlTest, GetViewTest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import views as auth_views
from . import views


class TestRegister(TestCase, ResolveUrlTest, GetViewTest):
    name = 'register'
    view = views.register
    template = 'accounts/register.html'
    status = 200

    def test_post_not_required_fields(self):
        client = Client()

        response = client.post(reverse(self.name), {})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEquals(len(User.objects.all()), 0)
        self.assertEquals(len(Profile.objects.all()), 0)

    def test_post_invalid_chars_in_username(self):
        client = Client()

        response = client.post(reverse(self.name), {'username': '#@@@@@@', 'password': 'thisisagoodpassword'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEquals(len(User.objects.all()), 0)
        self.assertEquals(len(Profile.objects.all()), 0)

    def test_post_username_invalid_to_short(self):
        client = Client()

        response = client.post(reverse(self.name), {'username': 'aa', 'password1': 'thisisagoodpassword', 'password2': 'thisisagoodpassword'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEquals(len(User.objects.all()), 0)
        self.assertEquals(len(Profile.objects.all()), 0)

    def test_post_username_invalid_to_long(self):
        client = Client()

        response = client.post(reverse(self.name), {'username': 'aaaaaaaaaaaaaaaaa', 'password1': 'thisisagoodpassword', 'password2': 'thisisagoodpassword'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEquals(len(User.objects.all()), 0)
        self.assertEquals(len(Profile.objects.all()), 0)

    def test_post_valid_username_password_without_recapture(self):
        client = Client()

        response = client.post(
            reverse(self.name),
            {
                'username': 'testuser1',
                'password1': 'thisisagoodpassword',
                'password2': 'thisisagoodpassword'
            }
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEquals(len(User.objects.all()), 0)
        self.assertEquals(len(Profile.objects.all()), 0)

    def test_post_valid_username_password_recapture(self):
        client = Client()

        response = client.post(
            reverse(self.name),
            {
                'username': 'testuser1',
                'password1': 'thisisagoodpassword',
                'password2': 'thisisagoodpassword',
                'g-recaptcha-response': 'PASSED'
            }
        )

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_URL))
        self.assertObjectExists(User, username='testuser1')
        self.assertObjectExists(Profile, user=User.objects.get(username='testuser1'))


class TestLogin(TestCase, ResolveUrlTest, GetViewTest):
    name = 'login'
    view = auth_views.LoginView
    template = 'accounts/login.html'
    status = 200

    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', password='password1')

    def test_post_not_all_required_fields(self):
        client = Client()

        response = client.post(reverse(self.name), {})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertNotIn('sessionid', response.cookies)

    def test_post_username_not_found(self):
        client = Client()

        response = client.post(reverse(self.name), {'username': 'testuser2', 'password': 'password2'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertNotIn('sessionid', response.cookies)

    def test_post_incorrect_password(self):
        client = Client()

        response = client.post(reverse(self.name), {'username': 'testuser1', 'password': 'password2'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertNotIn('sessionid', response.cookies)

    def test_post_successful_login(self):
        client = Client()

        response = client.post(reverse(self.name), {'username': 'testuser1', 'password': 'password1'})

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))
        self.assertIn('sessionid', response.cookies)


class TestLogout(TestCase, ResolveUrlTest, GetViewTest):
    name = 'logout'
    view = auth_views.LogoutView
    template = 'accounts/logout.html'
    status = 200

    def test_logged_out(self):
        user = User.objects.create_user(username='testuser1', password='password1')

        client = Client()
        client.login(username=user.username, password='password1')

        response = client.get(reverse(self.name))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/logout.html')
        self.assertFalse(response.context['user'].is_active)

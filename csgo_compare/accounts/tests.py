from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from firebrick.tests import BasicGETViewTest
from .models import Profile
from . import views


class TestRegister(TestCase, BasicGETViewTest):
    name = 'register'
    view = views.register
    template = 'accounts/register.html'
    status = 200
        
    def test_POST(self):      
        response = self.client.post(
            reverse(self.name),
            {
                'username': 'testuser1',
                'password1': 'thrkljrerfd',
                'password2': 'thrkljrerfd'
            }
        )
        
        self.assertObjectCreated(User, username='testuser1')
        self.assertObjectCreated(Profile, user=User.objects.filter(username='testuser1').first())
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_POST_invalid_username(self):
        response = self.client.post(
            reverse(self.name),
            {
                'username': 'this-username-is-invalid',
                'password1': 'thrkljrerfd',
                'password2': 'thrkljrerfd'
            }
        )
        
        self.assertObjectNotCreated(User, username='testuser1')
        self.assertObjectNotCreated(Profile, user=User.objects.filter(username='testuser1').first())
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)


class TestLogin(TestCase, BasicGETViewTest):
    name = 'login'
    view = auth_views.LoginView
    template = 'accounts/login.html'
    status = 200


        
class TestLogout(TestCase, BasicGETViewTest):
    name = 'logout'
    view = auth_views.LogoutView
    template = 'accounts/logout.html'
    status = 200

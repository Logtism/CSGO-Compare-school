from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from firebrick.tests import ResolveUrlTest, GetViewTest
from .models import SupportTicket, TicketReply
from . import views


class TestStat(TestCase, ResolveUrlTest, GetViewTest):
    name = 'info-stat'
    view = views.stat
    template = 'info/stat.html'
    status = 200
    
    
class TestAbout(TestCase, ResolveUrlTest, GetViewTest):
    name = 'info-about'
    view = views.about
    template = 'info/about.html'
    status = 200
    
    
class TestCreateTicket(TestCase, ResolveUrlTest):
    name = 'info-support-create'
    view = views.create_ticket
    template = 'info/create_ticket.html'
    
    def test_get_not_logged_in(self):
        client = Client()
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("login")}?next={reverse(self.name)}')
        
    def test_get_logged_in(self):
        user = User.objects.create_user(username='username1', password='password1')
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        
    def test_post_not_logged_in(self):
        client = Client()
        
        response = client.post(reverse(self.name))
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("login")}?next={reverse(self.name)}')
        
    def test_get_logged_in_no_form_data(self):
        user = User.objects.create_user(username='username1', password='password1')
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        
    def test_get_logged_in_valid_data(self):
        user = User.objects.create_user(username='username1', password='password1')
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.post(reverse(self.name), {'title': 'test title', 'body': 'this is some text'})
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('base-home'))
        
        self.assertObjectExists(SupportTicket, title='test title')
        
        
class TestTicketsList(TestCase, ResolveUrlTest):
    name = 'info-support'
    view = views.tickets_list
    template = 'info/tickets_list.html'
    
    def test_get_not_logged_in(self):
        client = Client()
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("login")}?next={reverse(self.name)}')
        
    def test_get_logged_in(self):
        user = User.objects.create_user(username='username1', password='password1')
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        
        
class TestViewTicket(TestCase, ResolveUrlTest):
    name = 'info-support-view'
    args = [1]
    view = views.view_ticket
    template = 'info/view_ticket.html'
    
    def setUp(self):
        self.user = User.objects.create_user(username='username1', password='password1')
        self.ticket = SupportTicket.objects.create(id=1, title='test', body='fsdfs', author=self.user)
    
    def test_get_not_logged_in(self):
        client = Client()
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("login")}?next={reverse(self.name, args=[1])}')
        
    def test_get_logged_in(self):
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        
    def test_post_not_logged_in(self):
        client = Client()
        
        response = client.post(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("login")}?next={reverse(self.name, args=[1])}')
        
    def test_get_logged_in_no_form_data(self):
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        
    def test_get_logged_in_valid_data(self):
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.post(reverse(self.name, args=[1]), {'body': 'this is some text'})
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        
        self.assertObjectExists(TicketReply, body='this is some text', ticket=self.ticket)
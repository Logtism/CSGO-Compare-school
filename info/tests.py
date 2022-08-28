from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
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


class TestFAQ(TestCase, ResolveUrlTest, GetViewTest):
    name = 'info-faq'
    view = views.faq
    template = 'info/faq.html'
    status = 200


class TestCreateTicket(TestCase, ResolveUrlTest):
    name = 'info-support-create'
    view = views.create_ticket
    template = 'info/create_ticket.html'

    def test_get_not_logged_in(self):
        client = Client()

        response = client.get(reverse(self.name))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse(self.name)}'
        )

    def test_get_logged_in(self):
        User.objects.create_user(username='username1', password='password1')

        client = Client()
        client.login(username='username1', password='password1')

        response = client.get(reverse(self.name))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_get_logged_in_no_form_data(self):
        User.objects.create_user(username='username1', password='password1')

        client = Client()
        client.login(username='username1', password='password1')

        response = client.get(reverse(self.name))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_post_not_logged_in(self):
        client = Client()

        response = client.post(reverse(self.name))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse(self.name)}'
        )

    def test_post_logged_in_valid_data(self):
        User.objects.create_user(username='username1', password='password1')

        client = Client()
        client.login(username='username1', password='password1')

        response = client.post(
            reverse(self.name),
            {
                'title': 'test title',
                'body': 'this is some text'
            }
        )

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
        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse(self.name)}'
        )

    def test_get_logged_in(self):
        User.objects.create_user(username='username1', password='password1')

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
        self.user = User.objects.create_user(
            username='username1',
            password='password1'
        )
        self.other = User.objects.create_user(
            username='username2',
            password='password1'
        )
        self.admin = User.objects.create_user(
            username='adminuser1',
            password='password1'
        )
        self.ticket = SupportTicket.objects.create(
            id=1,
            title='test',
            body='fsdfs',
            author=self.user
        )

    def test_get_not_logged_in(self):
        client = Client()

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse(self.name, args=[1])}'
        )

    def test_get_logged_in_other_user(self):
        client = Client()
        client.login(username='username2', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)

    def test_get_logged_in_user_that_created_ticket(self):
        client = Client()
        client.login(username='username1', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_get_has_permission_can_close_support_ticket(self):
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_close_support_ticket')
            ]
        )

        client = Client()
        client.login(username='adminuser1', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)

    def test_get_has_permission_can_reply_support_ticket(self):
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_reply_support_ticket')
            ]
        )

        client = Client()
        client.login(username='adminuser1', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)

    def test_get_has_permission_can_view_support_ticket(self):
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_view_support_ticket')
            ]
        )

        client = Client()
        client.login(username='adminuser1', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_post_not_logged_in(self):
        client = Client()

        response = client.post(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse(self.name, args=[1])}'
        )

    def test_post_logged_in_wrong_user(self):
        client = Client()
        client.login(username='username2', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)

    def test_post_logged_in_user_that_created_ticket_no_form_data(self):
        client = Client()
        client.login(username='username1', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_post_logged_in_user_that_created_ticket_valid_data(self):
        client = Client()
        client.login(username='username1', password='password1')

        response = client.post(
            reverse(self.name, args=[1]),
            {
                'body': 'this is some text'
            }
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

        self.assertObjectExists(
            TicketReply,
            body='this is some text',
            ticket=self.ticket
        )

    def test_post_has_permission_can_close_support_ticket(self):
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_close_support_ticket')
            ]
        )

        client = Client()
        client.login(username='adminuser1', password='password1')

        response = client.post(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)

    def test_post_has_permission_can_view_support_ticket(self):
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_view_support_ticket')
            ]
        )

        client = Client()
        client.login(username='adminuser1', password='password1')

        response = client.post(
            reverse(
                self.name,
                args=[1]
            ),
            {
                'body': 'this is some text'
            }
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

        self.assertObjectDoesNotExist(
            TicketReply,
            body='this is some text',
            ticket=self.ticket
        )

    def test_post_has_permission_can_reply_support_ticket_no_form_data(self):
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_reply_support_ticket')
            ]
        )
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_view_support_ticket')
            ]
        )

        client = Client()
        client.login(username='adminuser1', password='password1')

        response = client.post(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_post_has_permission_can_reply_support_ticket_valid_data(self):
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_reply_support_ticket'),
                Permission.objects.get(codename='can_view_support_ticket')
            ]
        )

        client = Client()
        client.login(username='adminuser1', password='password1')

        response = client.post(
            reverse(
                self.name,
                args=[1]
            ),
            {
                'body': 'this is some text'
            }
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

        self.assertObjectExists(
            TicketReply,
            body='this is some text',
            ticket=self.ticket
        )


class TestCloseTicket(TestCase, ResolveUrlTest):
    name = 'info-support-close'
    args = [1]
    view = views.close_ticket

    def setUp(self):
        self.user = User.objects.create_user(
            username='username1',
            password='password1'
        )
        self.other = User.objects.create_user(
            username='username2',
            password='password1'
        )
        self.admin = User.objects.create_user(
            username='adminuser1',
            password='password1'
        )
        self.ticket = SupportTicket.objects.create(
            id=1,
            title='test',
            body='fsdfs',
            author=self.user
        )

    def test_not_logged_in(self):
        client = Client()

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse(self.name, args=[1])}'
        )

    def test_logged_in_as_other_user(self):
        client = Client()
        client.login(username='username2', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 404)

    def test_logged_in_as_user_that_created_ticket(self):
        client = Client()
        client.login(username='username1', password='password1')

        response = client.post(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('base-home'))

    def test_has_can_view_support_ticket(self):
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_view_support_ticket')
            ]
        )

        client = Client()
        client.login(username='adminuser1', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 404)

    def test_has_can_reply_support_ticket(self):
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_reply_support_ticket')
            ]
        )

        client = Client()
        client.login(username='adminuser1', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 404)

    def test_has_can_close_support_ticket(self):
        self.admin.user_permissions.set(
            [
                Permission.objects.get(codename='can_close_support_ticket')
            ]
        )

        client = Client()
        client.login(username='adminuser1', password='password1')

        response = client.get(reverse(self.name, args=[1]))

        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, '/site_admin/support/')

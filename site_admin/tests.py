from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from firebrick.tests import ResolveUrlTest, GetViewTest
from items.models import Category, Subcategory, Item
from info.models import SupportTicket
from . import views


class TestDashboard(TestCase, ResolveUrlTest):
    name = 'admin-dashboard'
    view = views.dashboard
    template = 'site_admin/dashboard.html'
    
    def test_not_logged_in(self):
        client = Client()
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_logged_in(self):
        user = User.objects.create_user(username='username1', password='password1')
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_is_staff(self):
        user = User.objects.create_user(username='username1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
    
    
class TestItemDashboard(TestCase, ResolveUrlTest):
    name = 'admin-items'
    view = views.items
    template = 'site_admin/items.html'
    
    def test_not_logged_in(self):
        client = Client()
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_logged_in(self):
        user = User.objects.create_user(username='username1', password='password1')
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_is_staff(self):
        user = User.objects.create_user(username='username1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)

    def test_has_can_accept_item_sub(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_accept_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_has_can_delete_item_sub(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_decline_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_has_can_view_item_sub_permission(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_view_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)


class TestReviewItem(TestCase, ResolveUrlTest):
    name = 'admin-review-item'
    args = [1]
    view = views.review_item
    template = 'site_admin/review_item.html'
    
    def setUp(self):
        self.cat = Category.objects.create(name='cat')
        self.subcat = Subcategory.objects.create(name='subcat', category=self.cat)
        self.item = Item.objects.create(id=1, name='test item', icon='icon', icon_large='big icon', subcategory=self.subcat)    
    
    def test_not_logged_in(self):
        client = Client()
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_logged_in(self):
        user = User.objects.create_user(username='username1', password='password1')
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_is_staff(self):
        user = User.objects.create_user(username='username1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_has_can_accept_item_sub(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_accept_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_has_can_delete_item_sub(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_decline_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_has_can_view_item_sub_permission_id_does_not_exist(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_view_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[10]))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_has_can_view_item_sub_permission_id_does_exist(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_view_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        
        
class TestAcceptItem(TestCase, ResolveUrlTest):
    name = 'admin-review-item-accept'
    args = [1]
    view = views.item_accept
    
    def setUp(self):
        self.cat = Category.objects.create(name='cat')
        self.subcat = Subcategory.objects.create(name='subcat', category=self.cat)
        self.item = Item.objects.create(id=1, name='test item', icon='icon', icon_large='big icon', subcategory=self.subcat)    
    
    def test_not_logged_in(self):
        client = Client()
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_logged_in(self):
        user = User.objects.create_user(username='username1', password='password1')
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_is_staff(self):
        user = User.objects.create_user(username='username1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_has_can_delete_item_sub(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_decline_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_has_can_view_item_sub_permission(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_view_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[10]))
        
        self.assertEquals(response.status_code, 404)

    def test_has_can_accept_item_sub_id_does_not_exist(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_accept_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[10]))
        
        self.assertEquals(response.status_code, 404)

    def test_has_can_accept_item_sub_id_does_exist(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_accept_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('admin-items'))
        
        self.assertTrue(Item.objects.get(id=self.item.id).accepted)
        
        
class TestDeleteItem(TestCase, ResolveUrlTest):
    name = 'admin-review-item-delete'
    args = [1]
    view = views.item_delete
    
    def setUp(self):
        self.cat = Category.objects.create(name='cat')
        self.subcat = Subcategory.objects.create(name='subcat', category=self.cat)
        self.item = Item.objects.create(id=1, name='test item', icon='icon', icon_large='big icon', subcategory=self.subcat)    
    
    def test_not_logged_in(self):
        client = Client()
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_logged_in(self):
        user = User.objects.create_user(username='username1', password='password1')
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_is_staff(self):
        user = User.objects.create_user(username='username1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_has_can_accept_item_sub(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_accept_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_has_can_view_item_sub_permission(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_view_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[10]))
        
        self.assertEquals(response.status_code, 404)

    def test_has_can_delete_item_sub_id_does_not_exist(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_decline_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[10]))
        
        self.assertEquals(response.status_code, 404)

    def test_has_can_delete_item_sub_id_does_exist(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_decline_item_sub')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('admin-items'))
        
        self.assertObjectDoesNotExist(Item, id=1)
        
        
class TestSupportDashboard(TestCase, ResolveUrlTest):
    name = 'admin-support'
    view = views.support
    template = 'site_admin/support.html'
    
    def test_not_logged_in(self):
        client = Client()
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_logged_in(self):
        user = User.objects.create_user(username='username1', password='password1')
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_is_staff(self):
        user = User.objects.create_user(username='username1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)

    def test_has_can_reply_support_ticket(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_reply_support_ticket')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_has_can_close_support_ticket(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_close_support_ticket')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, self.template)
        
    def test_has_can_view_support_ticket_permission(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_view_support_ticket')])
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        
    def test_has_can_view_support_ticket_permission_not_empty(self):
        user = User.objects.create_user(username='username1', password='password1')
        user.user_permissions.set([Permission.objects.get(codename='can_view_support_ticket')])
        
        ticket = SupportTicket.objects.create(title='title', body='body', author=user)
        
        client = Client()
        client.login(username='username1', password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
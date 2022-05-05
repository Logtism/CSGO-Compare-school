from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from firebrick.tests import ResolveUrlTest, GetViewTest
from items.models import Category, Subcategory, Item
from . import views


class TestDashboard(TestCase, ResolveUrlTest, GetViewTest):
    name = 'items-admin-dashboard'
    view = views.dashboard
    template = 'items_admin/dashboard.html'
    status = 200
    
    
class TestReviewItem(TestCase, ResolveUrlTest):
    name = 'items-admin-item'
    args = [1]
    view = views.review_item
    
    def setUp(self):
        self.cat = Category.objects.create(name='cat')
        self.subcat = Subcategory.objects.create(name='subcat', category=self.cat)
        self.item = Item.objects.create(id=1, name='test item', icon='icon', icon_large='big icon', subcategory=self.subcat)
    
    def test_get_not_logged_in(self):
        user = User.objects.create_user(username='testuser1', password='password1')
        
        client = Client()
        client.login(username=user.username, password='password1')
        
        response = client.get(reverse(self.name, args=[self.item.id]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_get_is_staff(self):
        user = User.objects.create_user(username='testuser1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username=user.username, password='password1')
        
        response = client.get(reverse(self.name, args=[self.item.id]))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'items_admin/review_item.html')
        
    def test_get_item_id_does_not_exist(self):
        user = User.objects.create_user(username='testuser1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username=user.username, password='password1')
        
        response = client.get(reverse(self.name, args=[500]))
        
        self.assertEquals(response.status_code, 404)
        
        
    def test_post_update_item(self):
        user = User.objects.create_user(username='testuser1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username=user.username, password='password1')
        
        response = client.post(
            reverse(self.name, args=[self.item.id]),
            {
                'name': 'testing name 1',
                'icon': 'icon',
                'icon_large': 'big',
                'subcategory': self.subcat.id,
                'lowest_float': 0.0
            }
        )
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'items_admin/review_item.html')
        self.assertObjectExists(Item, name='testing name 1', icon='icon', icon_large='big', subcategory=self.subcat.id, lowest_float=0.0)
    
    
class TestAcceptItem(TestCase, ResolveUrlTest):
    name = 'items-admin-item-accept'
    args = [1]
    view = views.item_accept

    def setUp(self):
        self.cat = Category.objects.create(name='cat')
        self.subcat = Subcategory.objects.create(name='subcat', category=self.cat)
        self.item = Item.objects.create(id=1, name='test item', icon='icon', icon_large='big icon', subcategory=self.subcat)    

    def test_get_not_logged_in(self):
        user = User.objects.create_user(username='testuser1', password='password1')
        
        client = Client()
        client.login(username=user.username, password='password1')
        
        response = client.get(reverse(self.name, args=[self.item.id]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_get_is_staff(self):
        user = User.objects.create_user(username='testuser1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username=user.username, password='password1')
        
        response = client.get(reverse(self.name, args=[self.item.id]))
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('items-admin-item', args=[self.item.id]))
        self.assertObjectExists(Item, id=self.item.id, accepted=True)
        
    def test_get_item_id_does_not_exist(self):
        user = User.objects.create_user(username='testuser1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username=user.username, password='password1')
        
        response = client.get(reverse(self.name, args=[500]))
        
        self.assertEquals(response.status_code, 404)


class TestDeleteItem(TestCase, ResolveUrlTest):
    name = 'items-admin-item-delete'
    args = [1]
    view = views.item_delete
    
    def setUp(self):
        self.cat = Category.objects.create(name='cat')
        self.subcat = Subcategory.objects.create(name='subcat', category=self.cat)
        self.item = Item.objects.create(id=1, name='test item', icon='icon', icon_large='big icon', subcategory=self.subcat)
        
    def test_get_not_logged_in(self):
        user = User.objects.create_user(username='testuser1', password='password1')
        
        client = Client()
        client.login(username=user.username, password='password1')
        
        response = client.get(reverse(self.name, args=[self.item.id]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_get_is_staff(self):
        user = User.objects.create_user(username='testuser1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username=user.username, password='password1')
        
        response = client.get(reverse(self.name, args=[self.item.id]))
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('items-admin-dashboard'))
        self.assertObjectDoesNotExist(Item, id=self.item.id, accepted=True)
        
    def test_get_item_id_does_not_exist(self):
        user = User.objects.create_user(username='testuser1', password='password1', is_staff=True)
        
        client = Client()
        client.login(username=user.username, password='password1')
        
        response = client.get(reverse(self.name, args=[500]))
        
        self.assertEquals(response.status_code, 404)
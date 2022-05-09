from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from firebrick.tests import ResolveUrlTest
from accounts.models import Profile
from .models import Category, Subcategory, Rarity, Collection, Item
from . import views


class TestSubcat(TestCase, ResolveUrlTest):
    name = 'items-subcat'
    args = [0]
    view = views.subcat
    
    def test_id_does_not_exist(self):
        client = Client()
        
        response = client.get(reverse(self.name, args=[2]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_id_does_exist(self):
        cat = Category.objects.create(name='cat')
        subcat = Subcategory.objects.create(name='subcat', category=cat)
        # item = Item.objects.create(name='test item', icon='icon url', icon_large='big icon url', subcategory=subcat)
        
        client = Client()
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/subcat.html')
        

class TestCollection(TestCase, ResolveUrlTest):
    name = 'items-collection'
    args = [0]
    view = views.collection
    
    def test_id_does_not_exist(self):
        client = Client()
        
        response = client.get(reverse(self.name, args=[2]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_id_does_exist(self):
        collection = Collection.objects.create(id=1, name='test name', icon='icon', icon_large='big icon')
        
        client = Client()
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/collection.html')
        
        
class TestItem(TestCase, ResolveUrlTest):
    name = 'items-item'
    args = [0]
    view = views.item
    
    def test_id_does_not_exist(self):
        client = Client()
        
        response = client.get(reverse(self.name, args=[2]))
        
        self.assertEquals(response.status_code, 404)
        
    def test_id_does_exist_not_accepted(self):
        cat = Category.objects.create(name='cat')
        subcat = Subcategory.objects.create(name='subcat', category=cat)
        item = Item.objects.create(id=1, name='test item', icon='icon url', icon_large='big icon url', subcategory=subcat)
        
        client = Client()
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'items/item.html')
        
    def test_id_does_exist_accepted(self):
        cat = Category.objects.create(name='cat')
        subcat = Subcategory.objects.create(name='subcat', category=cat)
        item = Item.objects.create(id=1, name='test item', icon='icon url', icon_large='big icon url', accepted=True, subcategory=subcat)
        
        client = Client()
        
        response = client.get(reverse(self.name, args=[1]))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/item.html')


class TestAddItem(TestCase, ResolveUrlTest):
    name='items-add-item'
    view = views.add_item
    
    def setUp(self):
        self.cat = Category.objects.create(name='cat')
        self.subcat = Subcategory.objects.create(name='subcat', category=self.cat)
        self.rarity = Rarity.objects.create(name='good', color='#fff')
        self.collection = Collection.objects.create(name='test', icon='icon url', icon_large='big icon url')
        self.user = User.objects.create_user(username='testuser1', password='password1')
    
    def test_get_not_logged_in(self):
        client = Client()
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'/{settings.LOGIN_URL}/?next={reverse(self.name)}')
        
    def test_get_logged_in(self):
        client = Client()
        client.login(username=self.user.username, password='password1')
        
        response = client.get(reverse(self.name))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/add_item.html')
        
    def test_post_not_logged_in(self):
        client = Client()
        
        response = client.post(reverse(self.name))
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'/{settings.LOGIN_URL}/?next={reverse(self.name)}')
        
    def test_post_without_required_fields(self):
        client = Client()
        client.login(username=self.user.username, password='password1')
        
        response = client.post(reverse(self.name), {})
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/add_item.html')
        self.assertEquals(len(Item.objects.all()), 0)
    
    def test_with_only_required_fields(self):
        client = Client()
        client.login(username=self.user.username, password='password1')
        
        response = client.post(
            reverse(self.name),
            {
                'name': 'test_item',
                'icon': 'icon url',
                'icon_large': 'big icon url',
                'subcategory': self.subcat.id
            }
        )
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/add_item.html')
        
        self.assertObjectExists(
            Item,
            name='test_item',
            icon='icon url',
            icon_large='big icon url',
            accepted=False,
            added_by=Profile.objects.get(user=User.objects.get(username=self.user.username)),
            subcategory=self.subcat
        )
        
    def test_with_all_fields(self):
        client = Client()
        client.login(username=self.user.username, password='password1')
        
        response = client.post(
            reverse(self.name),
            {
                'name': 'test_item',
                'icon': 'icon url',
                'icon_large': 'big icon url',
                'lowest_float': 0.0,
                'highest_float': 0.999,
                'stattrak': True,
                'souvenir': False,
                'subcategory': self.subcat.id,
                'rarity': self.rarity.id,
                'collection': self.collection.id
            }
        )
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/add_item.html')
        
        self.assertObjectExists(
            Item,
            name='test_item',
            icon='icon url',
            icon_large='big icon url',
            lowest_float=0.0,
            highest_float = 0.999,
            stattrak=True,
            souvenir=False,
            accepted=False,
            added_by=Profile.objects.get(user=User.objects.get(username=self.user.username)),
            subcategory=self.subcat,
            rarity=self.rarity,
            collection=self.collection
        )
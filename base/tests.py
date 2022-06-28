from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command
from firebrick.tests import ResolveUrlTest
from . import views


class TestHome(TestCase, ResolveUrlTest):
    name = 'base-home'
    view = views.home
    template = 'base/home.html'

    def test_get(self):
        call_command('loaddata', 'catogory', 'subcategory', 'rarity', 'collection', 'container', 'item', verbosity=0)

        client = Client()

        response = client.get(reverse(self.name))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

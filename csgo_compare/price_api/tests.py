from django.test import TestCase, Client
from django.core.management import call_command
from firebrick.tests import ResolveUrlTest
from django.urls import reverse
from . import views


class TestSkinport(TestCase, ResolveUrlTest):
    name = 'price-api-skinport'
    view = views.skinport
    args = [1]

    def test_get_id_does_not_exist(self):
        client = Client()

        response = client.get(reverse(self.name, args=[9999]))

        self.assertEqual(response.status_code, 404)

        self.assertIn('success', response.json())
        self.assertFalse(response.json()['success'])
        self.assertIn('error_msg', response.json())
        self.assertEqual(
            response.json()['error_msg'],
            'Item id does not exist.'
        )

    def test_get_id_does_exist(self):
        call_command(
            'loaddata',
            'catogory',
            'subcategory',
            'collection',
            'container',
            'rarity',
            'pattern',
            'item',
            verbosity=0
        )

        client = Client()

        response = client.get(reverse(self.name, args=[1]))

        self.assertEqual(response.status_code, 200)

        self.assertIn('success', response.json())

        self.assertTrue(response.json()['success'])
        for wear_type in ['fn', 'mw', 'ft', 'ww', 'bs']:
            self.assertIn(wear_type, response.json())
            # Check if its a 0 if its not a float
            if type(response.json()[wear_type]) != float:
                self.assertEqual(type(response.json()[wear_type]), int)
                self.assertEqual(response.json()[wear_type], 0)
            else:
                self.assertEqual(type(response.json()[wear_type]), float)

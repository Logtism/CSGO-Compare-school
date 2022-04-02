from django.test import TestCase
from firebrick.tests import BasicGETViewTest
from . import views


class TestHome(TestCase, BasicGETViewTest):
    name = 'base-home'
    view = views.home
    template = 'base/home.html'
    status = 200


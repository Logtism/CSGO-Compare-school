from django.test import TestCase
from firebrick.tests import ResolveUrlTest, GetViewTest
from . import views


class TestHome(TestCase, ResolveUrlTest, GetViewTest):
    name = 'base-home'
    view = views.home
    template = 'base/home.html'
    status = 200
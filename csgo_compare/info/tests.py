from django.test import TestCase
from firebrick.tests import ResolveUrlTest, GetViewTest
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
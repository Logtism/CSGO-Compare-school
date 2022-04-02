from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='base-home'),
    path('home/', views.home, name='base-home'),
]

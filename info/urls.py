from django.urls import path
from . import views


urlpatterns = [
    path('statistics/', views.stat, name='info-stat'),
    path('about/', views.about, name='info-about'),
]

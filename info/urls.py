from django.urls import path
from . import views


urlpatterns = [
    path('statistics/', views.stat, name='info-stat'),
    path('about/', views.about, name='info-about'),
    path('support/create/', views.create_ticket, name='info-support-create'),
    path('support/', views.tickets_list, name='info-support'),
    path('support/<int:id>/', views.view_ticket, name='info-support-view')
]

from django.urls import path
from . import views


urlpatterns = [
    path('items/<int:id>/', views.items, name='items-items'),
    path('item/<int:id>/', views.item, name='items-item'),
    path('add/item/', views.add_item, name='items-add-item'),
]

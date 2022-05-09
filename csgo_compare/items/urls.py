from django.urls import path
from . import views


urlpatterns = [
    path('subcat/<int:id>/', views.subcat, name='items-subcat'),
    path('collection/<int:id>/', views.collection, name='items-collection'),
    path('item/<int:id>/', views.item, name='items-item'),
    path('add/item/', views.add_item, name='items-add-item'),
]

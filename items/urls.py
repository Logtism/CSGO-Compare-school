from django.urls import path
from . import views


urlpatterns = [
    path('subcat/<int:id>/', views.subcat, name='items-subcat'),
    path('collection/<int:id>/', views.collection, name='items-collection'),
    path('pattern/<int:id>/', views.pattern, name='items-pattern'),
    path('item/<int:id>/', views.item, name='items-item'),
    path('add/item/', views.add_item, name='items-add-item'),
]

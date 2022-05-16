from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='items-admin-dashboard'),
    path('item/<int:id>/', views.review_item, name='items-admin-item'),
    path('item/accept/<int:id>/', views.item_accept, name='items-admin-item-accept'),
    path('item/delete/<int:id>/', views.item_delete, name='items-admin-item-delete'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin-dashboard'),
    path('dashboard/', views.dashboard, name='admin-dashboard'),
    
    path('items/', views.items, name='admin-items'),
    path('items/<int:id>/', views.review_item, name='admin-review-item'),
    path('items/<int:id>/preview/', views.item_preview, name='admin-preview-item'),
    path('items/accept/<int:id>/', views.item_accept, name='admin-review-item-accept'),
    path('items/delete/<int:id>/', views.item_delete, name='admin-review-item-delete'),
    
    path('support/', views.support, name='admin-support'),
]

from django.urls import path
from . import views


urlpatterns = [
    path('skinport/<int:id>/', views.skinport, name='price-api-skinport'),
]

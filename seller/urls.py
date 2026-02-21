from django.urls import path
from seller import views

urlpatterns = [
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('password_change/', views.seller_password_change, name='seller_password_change'),
]
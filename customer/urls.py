from django.urls import path
from customer import views

urlpatterns = [
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('password_change/', views.customer_password_change, name='customer_password_change'),
]

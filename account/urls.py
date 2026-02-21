from django.urls import path
from account import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # user registeration
    path('register/', views.register_user, name='register_user'),
    
    # account activation mail
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate_account'),
    
    # user login
    path('login/', views.login_user, name='login_user'),

    # user logout
    path('logout', LogoutView.as_view(), name='logout_user'),

    # password reset
    path('password_reset/', views.password_reset, name='password_reset'),

    # password reset confirm
    path('password_reset_confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]

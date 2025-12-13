from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('', views.home_view, name='home_view'),
    path('api/check-role/', views.api_check_role, name='api_check_role'),
]
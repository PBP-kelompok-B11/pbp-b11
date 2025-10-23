from django.urls import path
from . import views

<<<<<<< HEAD
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('', views.home_view, name='home'),
=======
app_name = 'authentication'

urlpatterns = [
    path('register/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
     path('', views.home_view, name='home_view'),
>>>>>>> ad32ec64ac5e08c3c9ced140258fc6ce2b501355
]
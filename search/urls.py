# search/urls.py
from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_form, name='search_form'),
    path('json/', views.show_json, name='show_json'),
    path('go/', views.search_redirect, name='search_redirect'),
    path('players/', views.search_players, name='search_players'),
    path('clubs/', views.search_clubs, name='search_clubs'),
    path('events/', views.search_events, name='search_events'),
]
# search/urls.py
from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_form, name='search_form'),
    path('json/', views.show_json, name='show_json'),
    path('xml/', views.show_xml, name='show_xml'),
    
    path('players/', views.search_players, name='search_players'),
    path('clubs/', views.search_clubs, name='search_clubs'),
    path('history/', views.search_history, name='search_history'),
]

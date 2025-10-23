# search/urls.py
from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_form, name='search_form'),
    path('json/', views.show_json, name='show_json'),
    path('xml/', views.show_xml_by_id, name='show_xml'), #ini ubah nnti by id
    path('', views.search_redirect, name='search_redirect'),
    path('players/', views.search_players, name='search_players'),
    path('clubs/', views.search_clubs, name='search_clubs'),
    path('history/', views.search_history, name='search_history'),
    path('clear-history/', views.clear_search_history, name='clear_search_history'),
    path('events/', views.search_events, name='search_events'),
    path('events/filter/', views.filter_events, name='filter_events'),

]
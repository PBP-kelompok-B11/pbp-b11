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
    path('players/filter/', views.filter_players, name='filter_players'),
    path('clubs/filter/', views.filter_clubs, name='filter_clubs'),

]

#WHAT SHOULD I DO

# 1. Nambahin id di path urls
# 2. izin ke ibeth dan Ubah kode list.html yang ada di ibeth_club (include club_filter_component.html)
# 3. izin ke rafi dan Ubah kode list.html yang ada di rafi_player (include player_filter_component.html)
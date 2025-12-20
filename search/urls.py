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

    # ======================
    # API FLUTTER
    # ======================
    path('api/search/', views.api_search, name='api_search'),
    path('api/search/history/', views.api_history, name='api_search_history'),
    path('api/search/history/clear/', views.api_history_clear, name='api_history_clear'),
    path('api/search/history/<int:history_id>/', views.api_history_delete_item, name='api_history_delete_item'),
    path('api/search/suggest/', views.api_search_suggestion, name='api_search_suggestion'),

]

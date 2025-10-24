from django.urls import path
from . import views

app_name = 'rafi_player'

urlpatterns = [
    path('', views.player_list, name='player_list'),
    path('<uuid:id>/', views.player_detail, name='player_detail'),
    path('create/', views.player_create, name='player_create'),
    path('<uuid:id>/update/', views.player_update, name='player_update'),
    path('<uuid:id>/delete/', views.player_delete, name='player_delete'),
    path('json/', views.show_json_player, name='show_json_player'),
]

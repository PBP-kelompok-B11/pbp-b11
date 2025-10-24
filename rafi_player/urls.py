from django.urls import path
from . import views

app_name = 'rafi_player'

urlpatterns = [
    path('', views.player_list, name='player_list'),
    path("add-player-ajax/", views.add_player_ajax, name="add_player_ajax"),
    path('json/', views.show_json_player, name='show_json_player'),
    path('player/<uuid:player_id>/json/', views.show_json_player_by_id, name='show_json_player_by_id'),
    path('player/<uuid:player_id>/', views.player_detail, name='player_detail'),
    # path('player/<uuid:player_id>/edit/', views.edit_player, name='edit_player'),
    path('player/<uuid:player_id>/delete/', views.delete_player, name='delete_player'),
    # path('player/<uuid:player_id>/edit/', views.edit_player, name='edit_player'),
    # path('player/<int:pk>/edit/', views.edit_player_ajax, name='edit_player_ajax'),
    path('<uuid:pk>/edit/', views.edit_player_ajax, name='edit_player_ajax'),

]

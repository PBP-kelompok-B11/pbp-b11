from django.urls import path
from . import views

app_name = 'rafi_player'

urlpatterns = [
    path('', views.player_list, name='player_list'),
    path('<int:pk>/', views.player_detail, name='player_detail'),
    path('create/', views.player_create, name='player_create'),
    path('<int:pk>/update/', views.player_update, name='player_update'),
    path('<int:pk>/delete/', views.player_delete, name='player_delete'),
]

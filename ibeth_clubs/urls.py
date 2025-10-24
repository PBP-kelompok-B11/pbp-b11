from django.urls import path
from . import views

app_name = 'ibeth_clubs'

urlpatterns = [
    path('', views.club_list, name='club_list'),
    path('club/new/', views.club_create, name='club_create'),
    path('rankings/', views.ranking_list, name='ranking_list'),

    path('club/<int:pk>/', views.club_detail, name='club_detail'),
    path('club/<int:pk>/edit/', views.club_update, name='club_update'),
    path('club/<int:pk>/delete/', views.club_delete, name='club_delete'),

    path('club/<int:club_pk>/ranking/new/', views.club_ranking_create, name='club_ranking_create'),
    path('ranking/<int:pk>/edit/', views.club_ranking_update, name='club_ranking_update'),
    path('ranking/<int:pk>/delete/', views.club_ranking_delete, name='club_ranking_delete'),
]

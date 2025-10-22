from django.urls import path
from . import views

urlpatterns = [
    path('', views.club_list, name='club_list'),
    path('<int:pk>/', views.club_detail, name='club_detail'),
    path('create/', views.club_create, name='club_create'),
    path('<int:pk>/update/', views.club_update, name='club_update'),
    path('<int:pk>/delete/', views.club_delete, name='club_delete'),

    path('ranking/', views.ranking_list, name='club_ranking_list'),
    path('<int:club_pk>/ranking/create/', views.ranking_create, name='club_ranking_create'),
    path('ranking/<int:pk>/update/', views.ranking_update, name='club_ranking_update'),
    path('ranking/<int:pk>/delete/', views.ranking_delete, name='club_ranking_delete'),
]

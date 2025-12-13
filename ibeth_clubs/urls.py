from django.urls import path
from . import views
from .api import ClubListAPI, ClubDetailAPI 
from .api_ranking import RankingListAPI, RankingDetailAPI

app_name = 'ibeth_clubs'

urlpatterns = [
    path('', views.club_list, name='club_list'),
    path('<int:pk>/', views.club_detail, name='club_detail'),
    path('create/', views.club_create, name='club_create'),
    path('<int:pk>/edit/', views.club_update, name='club_update'),
    path('<int:pk>/delete/', views.club_delete, name='club_delete'),

    path('ranking/', views.ranking_list, name='ranking_list'),
    path('<int:club_pk>/ranking/create/', views.club_ranking_create, name='club_ranking_create'),
    path('ranking/<int:pk>/edit/', views.club_ranking_update, name='club_ranking_update'),
    path('ranking/<int:pk>/delete/', views.club_ranking_delete, name='club_ranking_delete'),

    path('api/', ClubListAPI.as_view(), name='club_list_api'),
    path('api/<int:pk>/', ClubDetailAPI.as_view(), name='club_detail_api'),

    path('ranking/api/', RankingListAPI.as_view(), name='ranking_list_api'),
    path('ranking/api/<int:pk>/', RankingDetailAPI.as_view(), name='ranking_detail_api'),

    path('api/', views.api_club_list_create),
    path('api/<int:pk>/', views.api_club_detail),

]

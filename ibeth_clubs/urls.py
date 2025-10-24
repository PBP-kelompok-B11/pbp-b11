from django.urls import path
from . import views

app_name = 'ibeth_clubs'

urlpatterns = [
    # Halaman utama daftar klub
    path('', views.club_list, name='club_list'),

    # CRUD untuk klub
    path('create/', views.club_create, name='club_create'),
    path('<int:pk>/', views.club_detail, name='club_detail'),
    path('<int:pk>/edit/', views.club_update, name='club_update'),
    path('<int:pk>/delete/', views.club_delete, name='club_delete'),

    # CRUD untuk ranking klub
    path('<int:club_pk>/ranking/create/', views.club_ranking_create, name='club_ranking_create'),
    path('ranking/<int:pk>/edit/', views.club_ranking_update, name='club_ranking_update'),
    path('ranking/<int:pk>/delete/', views.club_ranking_delete, name='club_ranking_delete'),
]

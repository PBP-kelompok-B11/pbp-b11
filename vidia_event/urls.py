# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # EVENT CRUD
    path('', views.event_list, name='event_list'),                                # daftar semua event
    path('<int:pk>/', views.event_detail, name='event_detail'),                   # detail event
    path('create/', views.event_create, name='event_create'),                     # tambah event
    path('<int:pk>/edit/', views.event_update, name='event_update'),              # edit event
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),            # hapus event

    # PARTICIPATION CRUD
    path('<int:event_pk>/participation/add/', views.participation_add, name='participation_add'),  # tambah partisipan
    path('participation/<int:pk>/edit/', views.participation_update, name='participation_update'), # edit partisipan
    path('participation/<int:pk>/delete/', views.participation_delete, name='participation_delete'), # hapus partisipan
    
]
# DI PROJEK UTAMA: TULIS path('events/', include('events.urls')),
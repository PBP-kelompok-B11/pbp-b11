# events/urls.py
from django.urls import path
from . import views

app_name = 'vidia_event'
urlpatterns = [
    # EVENT CRUD
    path('', views.event_list, name='event_list'),                                # daftar semua event
    path('event/<int:pk>/', views.event_detail, name='event_detail'),                   # detail event
    path('event/create/', views.event_create, name='event_create'),                     # tambah event
    path('event/<int:pk>/edit/', views.event_update, name='event_update'),              # edit event
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),            # hapus event

    # PARTICIPATION CRUD
    path('event/<int:event_pk>/participation/add/', views.participation_add, name='participation_add'),  # tambah partisipan
    path('event/participation/<int:pk>/edit/', views.participation_update, name='participation_update'), # edit partisipan
    path('event/participation/<int:pk>/delete/', views.participation_delete, name='participation_delete'), # hapus partisipan
    
]
# DI PROJEK UTAMA: TULIS path('events/', include('events.urls')),
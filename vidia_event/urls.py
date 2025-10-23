# events/urls.py
from django.urls import path
from . import views

app_name = 'vidia_event'
urlpatterns = [
    # EVENT CRUD
    path('', views.event_list, name='event_list'),                                # daftar semua event
<<<<<<< HEAD
    path('event/<int:pk>/', views.event_detail, name='event_detail'),                   # detail event
    path('event/create/', views.event_create, name='event_create'),                     # tambah event
    path('event/<int:pk>/edit/', views.event_update, name='event_update'),              # edit event
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),            # hapus event
=======
    path('<int:pk>/', views.event_detail, name='event_detail'),                   # detail event
    path('create/', views.event_create, name='event_create'),                     # tambah event
    path('<int:pk>/edit/', views.event_update, name='event_update'),              # edit event
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),            # hapus event
>>>>>>> ef1b59a86dabf23991d6d6bc49820b3fced4cc57

    # PARTICIPATION CRUD
    path('<int:event_pk>/participation/add/', views.participation_add, name='participation_add'),  # tambah partisipan
    path('participation/<int:pk>/edit/', views.participation_update, name='participation_update'), # edit partisipan
    path('participation/<int:pk>/delete/', views.participation_delete, name='participation_delete'), # hapus partisipan
    
]
# DI PROJEK UTAMA: TULIS path('events/', include('events.urls')),
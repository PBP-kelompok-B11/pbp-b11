# events/urls.py
from django.urls import path
from . import views

app_name = 'vidia_event'

urlpatterns = [
    # EVENT CRUD
    path('', views.event_list, name='event_list'),                     # daftar semua event
    path('create/', views.event_create, name='event_create'),          # tambah event
    path('<int:pk>/', views.event_detail, name='event_detail'),        # detail event
    path('<int:pk>/edit/', views.event_update, name='event_update'),   # edit event
    path('<int:pk>/delete/', views.event_delete, name='event_delete'), # hapus event
]

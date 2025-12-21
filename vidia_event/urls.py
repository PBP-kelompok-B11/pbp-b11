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
    path('json/', views.show_event_json, name='show_event_json'), # daftar event dalam json
    path('create-flutter/', views.create_event_flutter, name='create_event_flutter'),
    path('my-events-json', views.my_events_json, name='my_events_json'),
    path('<int:pk>/edit-flutter/', views.edit_event_flutter, name='edit_event_flutter'),
    path('club-logo/<str:filename>/', views.club_logo, name='club_logo'),
]

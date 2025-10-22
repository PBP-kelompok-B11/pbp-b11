<<<<<<< HEAD:search/urls.py
# search/urls.py
from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_form, name='search_form'),
    path('json/', views.show_json, name='show_json'),
    path('xml/', views.show_xml, name='show_xml'),
    
    path('players/', views.search_players, name='search_players'),
    path('clubs/', views.search_clubs, name='search_clubs'),
    path('history/', views.search_history, name='search_history'),
=======
from django.urls import path
from . import views

app_name = 'nina_media_gallery'

urlpatterns = [
    path('', views.gallery_list, name='gallery_list'),
    path('upload-media/', views.gallery_upload, name='gallery_upload'),
    path('media/<uuid:id>/update', views.gallery_update, name='gallery_update'),
    path('media/<uuid:id>/delete', views.gallery_delete, name='gallery_delete'),
>>>>>>> 13ec1a0ace631279e2cc8a43e1d06b7afdacbc3d:nina_media_gallery/urls.py
]

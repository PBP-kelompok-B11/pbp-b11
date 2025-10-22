from django.urls import path
from . import views

app_name = 'nina_media_gallery'

urlpatterns = [
    path('', views.gallery_list, name='gallery_list'),
    path('upload-media/', views.gallery_upload, name='gallery_upload'),
    path('media/<uuid:id>/update', views.gallery_update, name='gallery_update'),
    path('media/<uuid:id>/delete', views.gallery_delete, name='gallery_delete'),
]

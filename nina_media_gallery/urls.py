from django.urls import path
from . import views

app_name = 'nina_media_gallery'

urlpatterns = [
    path('', views.gallery_list, name='gallery_list'),
    path('upload-media/', views.gallery_upload, name='gallery_upload'),
    path('api/items/', views.get_gallery_items, name='get_gallery_items'),
    path('<uuid:id>/update/', views.gallery_update, name='gallery_update'),
    path('<uuid:id>/delete/', views.gallery_delete, name='gallery_delete'),
    path('<uuid:id>/', views.gallery_details, name='gallery_details'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:product_id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_id>/', views.show_json_by_id, name='show_json_by_id'),
    path('proxy-image/', views.proxy_image, name='proxy_image'),
    path('add-flutter/', views.add_media_flutter, name='add_media_flutter'),
]
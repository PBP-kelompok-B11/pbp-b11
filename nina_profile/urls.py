from django.urls import path
from . import views

app_name = 'nina_profile'

urlpatterns = [
    path('<str:target_model>/<int:pk>/', views.profile_overview, name='profile_overview'),
    path('admin/widgets/', views.widget_list, name='widget_list'),
    path('widget/create/', views.widget_create, name='widget_create'),
    path('widget/<int:pk>/update/', views.widget_update, name='widget_update'),
    path('widget/<int:pk>/delete/', views.widget_delete, name='widget_delete'),
]
from django.urls import path
from .views import comment_add, comment_list, add_comment_to_event, edit_comment, delete_comment

app_name = 'comments'

urlpatterns = [
    path('<str:app_label>/<str:model_name>/<int:object_id>/', comment_list, name='comment_list'),
    path('<str:model_name>/<int:object_id>/add/', comment_add, name='comment_add'),
    path('edit/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('event/<int:event_id>/add/', add_comment_to_event, name='add_comment_to_event'),
]
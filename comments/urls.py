from django.urls import path
from .views import comment_add, comment_list, comment_update, comment_delete, add_comment_to_event

app_name = 'comments'

urlpatterns = [
    path('<str:model_name>/<int:object_id>/', comment_list, name='comment_list'),
    path('<str:model_name>/<int:object_id>/add/', comment_add, name='comment_add'),
    path('update/<int:comment_id>/', comment_update, name='comment_update'),
    path('delete/<int:comment_id>/', comment_delete, name='comment_delete'),
    path('event/<int:event_id>/add/', add_comment_to_event, name='add_comment_to_event'),
]
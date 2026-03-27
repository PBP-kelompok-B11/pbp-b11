from django.urls import path
from .views import comment_list, add_comment_to_event, edit_comment, delete_comment, add_comment_to_club, add_comment_to_player, player_comments_json, club_comments_json, event_comments_json, comment_list_flutter, add_comment_flutter, edit_comment_flutter, delete_comment_flutter

app_name = 'comments'

urlpatterns = [
    path('<str:app_label>/<str:model_name>/<int:object_id>/', comment_list, name='comment_list'),
    path('edit/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('event/<int:event_id>/add/', add_comment_to_event, name='add_comment_to_event'),
    path('club/<int:club_id>/add/', add_comment_to_club, name='add_comment_to_club'),
    path('player/<uuid:player_id>/add/', add_comment_to_player, name='add_comment_to_player'),
    path('json/player/<uuid:player_id>/', player_comments_json),
    path('json/event/<int:event_id>/', event_comments_json),
    path('json/club/<int:club_id>/', club_comments_json),

    path('flutter/<str:type>/<str:target_id>/', comment_list_flutter),
    path('flutter/add/<str:type>/<str:target_id>/', add_comment_flutter),
    path('flutter/edit/<int:comment_id>/', edit_comment_flutter),
    path('flutter/delete/<int:comment_id>/', delete_comment_flutter),
]
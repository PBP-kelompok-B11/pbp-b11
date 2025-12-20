from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Comments
from .forms import CommentForm
from rafi_player.models import Player
from vidia_event.models import Event
from ibeth_clubs.models import Club
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.utils.timezone import localtime

@login_required(login_url='/login/')
def add_comment_to_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_object = event
            comment.user = request.user
            comment.save()
            return redirect('vidia_event:event_detail', pk=event.id)
    else:
        form = CommentForm()
    return render(request, 'comments/form.html', {'form': form, 'form_action': request.path})

@login_required(login_url='/login/')
def add_comment_to_club(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_object = club
            comment.user = request.user
            comment.save()
            return redirect('ibeth_clubs:club_detail', pk=club.id)
    else:
        form = CommentForm()
    return render(request, 'comments/form.html', {'form': form, 'form_action': request.path})

@login_required(login_url='/login/')
def add_comment_to_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_object = player
            comment.user = request.user
            comment.save()
            return redirect('rafi_player:player_detail', player_id=player.id)
    else:
        form = CommentForm()
    return render(request, 'comments/form.html', {'form': form, 'form_action': request.path})

def comment_list(request, app_label, model_name, object_id):

    content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    comments = Comments.objects.filter(content_type=content_type, object_id=object_id).order_by('-tanggal')

    return render(request, 'comments/list.html', {
        'comments': comments,
        'model_name': model_name,
        'object_id': object_id,
    })


@login_required(login_url='/login/')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            # Dapatkan nama model dalam huruf kecil (e.g., 'event', 'player', 'club')
            model_name = comment.content_type.model
            
            # Dapatkan PK dari objek yang dikomentari
            object_pk = comment.object_id 
            
            # Tentukan nama URL berdasarkan nama model
            if model_name == 'event':
                redirect_url_name = 'vidia_event:event_detail'
            elif model_name == 'player':
                redirect_url_name = 'rafi_player:player_detail'
                return redirect(redirect_url_name, player_id=object_pk)
            elif model_name == 'club':
                redirect_url_name = 'ibeth_clubs:club_detail'
            else:
                return redirect('/') 

            return redirect(redirect_url_name, pk=object_pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comments/form.html', {'form': form})

@login_required(login_url='/login/')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id, user=request.user)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def player_comments_json(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    content_type = ContentType.objects.get_for_model(Player)

    comments = Comments.objects.filter(
        content_type=content_type,
        object_id=player.id
    ).select_related('user').order_by('-tanggal')

    return JsonResponse({
        "target": {
            "type": "player",
            "id": player.id,
            "name": player.nama,
        },
        "comments": [
            {
                "id": c.id,
                "user": {
                    "id": c.user.id,
                    "username": c.user.username,
                },
                "isi_komentar": c.isi_komentar,
                "tanggal": localtime(c.tanggal).isoformat(),
                "can_edit": request.user.is_authenticated and request.user == c.user
            }
            for c in comments
        ]
    })
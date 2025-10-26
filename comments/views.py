from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Comments
from .forms import CommentForm
from rafi_player.models import Player
from vidia_event.models import Event
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.http import JsonResponse

def refresh_comments(request, model_name, object_id):
    """Mengembalikan daftar komentar terbaru dalam bentuk HTML (untuk AJAX)."""
    content_type = ContentType.objects.get(model=model_name)
    comments = Comments.objects.filter(
        content_type=content_type,
        object_id=object_id
    ).order_by('-tanggal')

    html = render_to_string('comments/_comment_items.html', {'comments': comments})
    return JsonResponse({'html': html})

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

def comment_list(request, app_label, model_name, object_id):

    content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    comments = Comments.objects.filter(content_type=content_type, object_id=object_id).order_by('-tanggal')

    return render(request, 'comments/list.html', {
        'comments': comments,
        'model_name': model_name,
        'object_id': object_id,
    })

@login_required
def comment_add(request, model_name, object_id):
    if request.method == 'POST':
        isi_komentar = request.POST.get('isi_komentar')

        # Cari content type berdasarkan nama model (Player, Club, dll)
        content_type = ContentType.objects.get(model=model_name.lower())

        Comments.objects.create(
            user=request.user,
            isi_komentar=isi_komentar,
            content_type=content_type,
            object_id=object_id
        )

        return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('vidia_event:event_detail', pk=comment.content_object.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comments/form.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id, user=request.user)
    event_id = comment.content_object.id
    comment.delete()
    return redirect('vidia_event:event_detail', pk=event_id)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Comments
from rafi_player.models import Player

def comment_list(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    comments = Comments.objects.filter(player=player).order_by('-tanggal')
    return render(request, 'comments/list.html', {'player': player, 'comments': comments})


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
def comment_update(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id, user=request.user)

    if request.method == 'POST':
        comment.isi_komentar = request.POST.get('isi_komentar')
        comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'comments/form.html', {'comment': comment})


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id, user=request.user)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

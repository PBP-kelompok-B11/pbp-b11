from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import EventForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from comments.models import Comments
from comments.forms import CommentForm

# =========================
# EVENT CRUD VIEWS
# =========================

def event_list(request):
    """Menampilkan daftar semua event sepak bola."""
    events = Event.objects.all().order_by('-tanggal')  # pakai tanggal
    paginator = Paginator(events, 5)  # tampilkan 5 per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'event_list.html', {'page_obj': page_obj})


def event_detail(request, pk):
    """Menampilkan detail event tertentu beserta komentarnya."""
    event = get_object_or_404(Event, pk=pk)
    comments = Comments.objects.filter(
        content_type__model='event',
        object_id=event.id
    ).order_by('-tanggal')
    form = CommentForm()
    return render(request, 'event_detail.html', {
        'event': event,
        'comments': comments,
        'form': form,
    })


@login_required(login_url='/login/')
def event_create(request):
    if request.method == 'POST':
        location = request.POST.get('lokasi')
        date_str = request.POST.get('tanggal')
        tim_home = request.POST.get('tim_home')
        tim_away = request.POST.get('tim_away')
        skor_home = request.POST.get('skor_home')
        skor_away = request.POST.get('skor_away')
        if tim_home and tim_away:
            event_name = f"{tim_home} vs {tim_away}"
        else:
            # fallback kalau salah satu kosong
            event_name = "Event Tanpa Nama"
        event = Event.objects.create(
            nama_event=event_name,
            lokasi=location,
            tanggal=date_str if date_str else None,
            tim_home=tim_home,
            tim_away=tim_away,
            skor_home=int(skor_home) if skor_home else None,
            skor_away=int(skor_away) if skor_away else None,
            created_by=request.user
        )
        return redirect('vidia_event:event_list')

    return render(request, 'event_create.html')


@login_required(login_url='/login/')
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if not (request.user == event.created_by or request.user.is_staff):
        return HttpResponseForbidden("Anda tidak punya akses untuk mengedit event ini.")

    if request.method == 'POST':
        event.lokasi = request.POST.get('lokasi')
        event.tanggal = request.POST.get('tanggal')
        event.tim_home = request.POST.get('tim_home')
        event.tim_away = request.POST.get('tim_away')
        skor_home = request.POST.get('skor_home')
        skor_away = request.POST.get('skor_away')
        event.skor_home = int(skor_home) if skor_home else None
        event.skor_away = int(skor_away) if skor_away else None
        event.tim_away = request.POST.get('tim_away')
        event.tim_away = request.POST.get('tim_away')
        if event.tim_home and event.tim_away:
            event.nama_event = f"{event.tim_home} vs {event.tim_away}"
        else:
            # fallback kalau salah satu kosong
            event.nama_event = "Event Tanpa Nama"
        event.save()
        return redirect('vidia_event:event_detail', pk=event.pk)

    context = {
        'is_update': True,
        'event': event,
    }
    return render(request, 'event_create.html', context)


@login_required(login_url='/login/')
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('vidia_event:event_list')
    return render(request, 'event_delete.html', {'event': event})

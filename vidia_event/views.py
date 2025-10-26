# events/views.py
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm


# =========================
# EVENT CRUD VIEWS
# =========================

def event_list(request):
    """Menampilkan daftar semua event sepak bola."""
    events = Event.objects.all().order_by('-tanggal')
    paginator = Paginator(events, 5)  # tampilkan 5 per halaman

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'event_list.html', {'page_obj': page_obj})


def event_detail(request, pk):
    """Menampilkan detail event tertentu."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {
        'event': event,
    })


@login_required(login_url='/login/')
def event_create(request):
    """Membuat event baru."""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('vidia_event:event_list')
    else:
        form = EventForm()

    return render(request, 'event_create.html', {'form': form})


@login_required(login_url='/login/')
def event_update(request, pk):
    """Mengedit event yang sudah ada."""
    event = get_object_or_404(Event, pk=pk)

    # hanya creator atau admin yang boleh edit
    if not (request.user == event.created_by or request.user.is_staff):
        return HttpResponseForbidden("Anda tidak punya akses untuk mengedit event ini.")

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('vidia_event:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'event_create.html', {
        'form': form,
        'is_update': True,
        'event': event,
    })


@login_required(login_url='/login/')
def event_delete(request, pk):
    """Menghapus event."""
    event = get_object_or_404(Event, pk=pk)

    # hanya creator atau admin yang boleh hapus
    if not (request.user == event.created_by or request.user.is_staff):
        return HttpResponseForbidden("Anda tidak punya akses untuk menghapus event ini.")

    if request.method == 'POST':
        event.delete()
        return redirect('vidia_event:event_list')

    return render(request, 'event_delete.html', {'event': event})

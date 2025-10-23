from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Event, EventParticipation
from .forms import EventForm, EventParticipationForm


# =========================
# EVENT CRUD VIEWS
# =========================

def event_list(request):
    """Menampilkan daftar semua event sepak bola."""
    events = Event.objects.all().order_by('-tanggal_mulai')
    return render(request, 'event_list.html', {'events': events})


def event_detail(request, pk):
    """Menampilkan detail event tertentu beserta partisipannya."""
    event = get_object_or_404(Event, pk=pk)
    participations = EventParticipation.objects.filter(event=event)
    return render(request, 'event_detail.html', {
        'event': event,
        'participations': participations,
    })


def event_create(request):
    """Menambahkan event baru."""
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'event_form.html', {
        'form': form,
        'title': 'Tambah Event',
    })


def event_update(request, pk):
    """Mengedit informasi event."""
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_detail', pk=pk)
    return render(request, 'event_form.html', {
        'form': form,
        'title': 'Edit Event',
        'event': event,
    })


def event_delete(request, pk):
    """Menghapus event."""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'event_delete.html', {'event': event})


# =========================
# PARTICIPATION CRUD VIEWS
# =========================

def participation_add(request, event_pk):
    """Menambahkan partisipan ke event tertentu."""
    event = get_object_or_404(Event, pk=event_pk)
    form = EventParticipationForm(request.POST or None)
    if form.is_valid():
        participation = form.save(commit=False)
        participation.event = event
        participation.save()
        return redirect('event_detail', pk=event_pk)
    return render(request, 'participation_form.html', {
        'participation_form': form,
        'event': event,
        'title': 'Tambah Partisipan',
    })


def participation_update(request, pk):
    """Mengedit informasi partisipan."""
    participation = get_object_or_404(EventParticipation, pk=pk)
    form = EventParticipationForm(request.POST or None, instance=participation)
    if form.is_valid():
        form.save()
        return redirect('event_detail', pk=participation.event.pk)
    return render(request, 'participation_form.html', {
        'participation_form': form,
        'event': participation.event,
        'title': 'Edit Partisipan',
    })


def participation_delete(request, pk):
    """Menghapus partisipan dari event."""
    participation = get_object_or_404(EventParticipation, pk=pk)
    event_pk = participation.event.pk
    if request.method == 'POST':
        participation.delete()
        return redirect('event_detail', pk=event_pk)
    return render(request, 'participation_delete.html', {
        'participation': participation,
        'event': participation.event,
    })

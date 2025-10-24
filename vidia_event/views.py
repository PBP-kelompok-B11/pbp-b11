from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Event
from .forms import EventForm
from django.core.paginator import Paginator


# =========================
# EVENT CRUD VIEWS
# =========================

def event_list(request):
    """Menampilkan daftar semua event sepak bola."""
    events = Event.objects.all().order_by('-tanggal_selesai')
    paginator = Paginator(events, 5)  # tampilkan 5 per halaman

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'event_list.html', {'page_obj': page_obj})


def event_detail(request, pk):
    """Menampilkan detail event tertentu beserta partisipannya."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {
        'event': event,
    })

def event_create(request):
    if request.method == 'POST':
        event_name = request.POST.get('event')
        club_name = request.POST.get('clubs')
        player_name = request.POST.get('players')
        captain_name = request.POST.get('captain')
        winner_name = request.POST.get('winner')

        # --- cari event berdasarkan nama ---
        event = Event.objects.filter(nama_event__iexact=event_name).first()
        if not event:
            # Kalau event belum ada, buat baru
            event = Event.objects.create(
                nama_event=event_name,
                tipe='pertandingan',
                lokasi='Unknown',
                tanggal_mulai='2025-01-01',
                tanggal_selesai='2025-01-01'
            )

        # --- buat participation untuk club ---
        if club_name:
            club = Club.objects.filter(name__iexact=club_name).first()
            if club:
                EventParticipation.objects.create(
                    event=event,
                    club=club,
                    peran='klub',
                    hasil='kalah'
                )

        # --- buat participation untuk player ---
        if player_name:
            player = Player.objects.filter(name__iexact=player_name).first()
            if player:
                EventParticipation.objects.create(
                    event=event,
                    player=player,
                    peran='pemain',
                    hasil='kalah'
                )

        # --- buat participation untuk captain ---
        if captain_name:
            captain = Player.objects.filter(name__iexact=captain_name).first()
            if captain:
                EventParticipation.objects.create(
                    event=event,
                    player=captain,
                    peran='kapten',
                    hasil='kalah'
                )

        # --- buat participation untuk winner ---
        if winner_name:
            # coba cari di Club dulu, kalau ga ada coba Player
            winner_club = Club.objects.filter(name__iexact=winner_name).first()
            winner_player = Player.objects.filter(name__iexact=winner_name).first()

            if winner_club:
                EventParticipation.objects.create(
                    event=event,
                    club=winner_club,
                    peran='klub',
                    hasil='juara'
                )
            elif winner_player:
                EventParticipation.objects.create(
                    event=event,
                    player=winner_player,
                    peran='pemain',
                    hasil='juara'
                )

        # setelah semua berhasil disimpan
        return redirect('event_list')  # ubah ke halaman list event kamu

    # kalau GET request
    return render(request, 'event_create.html')



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



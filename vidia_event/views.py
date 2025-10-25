from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Event
from .forms import EventForm
from django.core.paginator import Paginator
from authentication.views import admin_only
from django.contrib.auth.decorators import login_required


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

@login_required(login_url='/login/')
def event_create(request):
    if request.method == 'POST':
        event_name = request.POST.get('event')
        type_name = request.POST.get('tipe')
        location = request.POST.get('lokasi')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # --- cari event berdasarkan nama ---
        event = Event.objects.filter(nama_event__iexact=event_name).first()
        if not event:
            # Kalau event belum ada, buat baru
            event = Event.objects.create(
                nama_event=event_name,
                tipe=type_name,
                lokasi=location,
                tanggal_mulai=start_date,
                tanggal_selesai=end_date,
            )

        # setelah semua berhasil disimpan
        return redirect('vidia_event:event_list')  # ubah ke halaman list event kamu

    # kalau GET request
    return render(request, 'event_create.html')

@login_required(login_url='/login/')
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        # Parsing string dari form (YYYY-MM-DD) menjadi date
        event.nama_event = request.POST.get('event')
        event.tipe = request.POST.get('tipe')
        event.lokasi = request.POST.get('lokasi')

        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if start_date_str:
            event.tanggal_mulai = start_date_str  # Django bisa parse 'YYYY-MM-DD' otomatis
        if end_date_str:
            event.tanggal_selesai = end_date_str

        event.save()
        return redirect('vidia_event:event_detail', pk=event.pk)

    # Pre-fill form dengan data event, convert tanggal ke format YYYY-MM-DD
    context = {
        'is_update': True,
        'event': event,
        'start_date': event.tanggal_mulai.strftime('%Y-%m-%d') if event.tanggal_mulai else '',
        'end_date': event.tanggal_selesai.strftime('%Y-%m-%d') if event.tanggal_selesai else '',
    }
    return render(request, 'event_create.html', context)

@login_required(login_url='/login/')
def event_delete(request, pk):
    """Menghapus event."""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('vidia_event:event_list')
    return render(request, 'event_delete.html', {'event': event})


# =========================
# PARTICIPATION CRUD VIEWS
# =========================
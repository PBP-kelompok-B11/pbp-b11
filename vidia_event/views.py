from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Event
from .forms import EventForm
from django.core.paginator import Paginator
from authentication.views import admin_only

# =========================
# EVENT CRUD VIEWS
# =========================

def event_list(request):
    """Menampilkan daftar semua event sepak bola."""
    events = Event.objects.all().order_by('-tanggal_selesai')
    paginator = Paginator(events, 5)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'event_list.html', {'page_obj': page_obj})


def event_detail(request, pk):
    """Menampilkan detail event tertentu beserta partisipannya."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {
        'event': event,
    })

@admin_only
def event_create(request):
    if request.method == 'POST':
        event_name = request.POST.get('event')
        type_name = request.POST.get('tipe')
        location = request.POST.get('lokasi')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')


        event = Event.objects.filter(nama_event__iexact=event_name).first()
        if not event:
           
            event = Event.objects.create(
                nama_event=event_name,
                tipe=type_name,
                lokasi=location,
                tanggal_mulai=start_date,
                tanggal_selesai=end_date,
            )

        
        return redirect('vidia_event:event_list')  

    # kalau GET request
    return render(request, 'event_create.html')

@admin_only
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.nama_event = request.POST.get('event')
        event.tipe = request.POST.get('tipe')
        event.lokasi = request.POST.get('lokasi')
        event.tanggal_mulai = request.POST.get('start_date')
        event.tanggal_selesai = request.POST.get('end_date')
        event.save()
        return redirect('vidia_event:event_detail', pk=event.pk)

    # Pre-fill form dengan data event
    context = {
        'is_update': True,
        'event': event
    }
    return render(request, 'event_create.html', context)

@admin_only
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



from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from authentication.views import admin_only
from comments.models import Comments
from comments.forms import CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.core import serializers
from django.http import HttpResponse, JsonResponse
import json
import os
from django.http import FileResponse, Http404

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_DIR = os.path.join(BASE_DIR, 'vidia_event', 'data', 'logos')

def club_logo(request, filename):
    file_path = os.path.join(LOGO_DIR, filename)

    if not os.path.exists(file_path):
        raise Http404("Logo not found")

    return FileResponse(open(file_path, 'rb'), content_type='image/png')

def event_list(request):
    """Menampilkan daftar semua event sepak bola."""
    events = Event.objects.all().order_by('-tanggal')
    paginator = Paginator(events, 5)
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
@admin_only
def event_create(request):
    if request.method == 'POST':
        skor_h = request.POST.get('skor_home')
        skor_a = request.POST.get('skor_away')
        
        # Logic: Jika string kosong, simpan sebagai None (NULL di DB)
        skor_home = int(skor_h) if skor_h and skor_h.strip() != "" else None
        skor_away = int(skor_a) if skor_a and skor_a.strip() != "" else None
        
        tim_home = request.POST.get('tim_home')
        tim_away = request.POST.get('tim_away')
        event_name = f"{tim_home} vs {tim_away}" if tim_home and tim_away else "Event Tanpa Nama"

        Event.objects.create(
            nama_event=event_name,
            lokasi=request.POST.get('lokasi'),
            tanggal=request.POST.get('tanggal') or None,
            tim_home=tim_home,
            tim_away=tim_away,
            skor_home=skor_home,
            skor_away=skor_away,
            created_by=request.user
        )
        return redirect('vidia_event:event_list')
    return render(request, 'event_create.html')

@login_required(login_url='/login/')
@admin_only
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not (request.user == event.created_by or request.user.is_staff):
        return HttpResponseForbidden("Akses ditolak.")

    if request.method == 'POST':
        skor_h = request.POST.get('skor_home')
        skor_a = request.POST.get('skor_away')
        
        event.lokasi = request.POST.get('lokasi')
        event.tanggal = request.POST.get('tanggal')
        event.tim_home = request.POST.get('tim_home')
        event.tim_away = request.POST.get('tim_away')
        
        # Handle Nullable Score
        event.skor_home = int(skor_h) if skor_h and skor_h.strip() != "" else None
        event.skor_away = int(skor_a) if skor_a and skor_a.strip() != "" else None
        
        event.nama_event = f"{event.tim_home} vs {event.tim_away}" if event.tim_home and event.tim_away else "Event Tanpa Nama"
        event.save()
        return redirect('vidia_event:event_detail', pk=event.pk)

    return render(request, 'event_create.html', {'is_update': True, 'event': event})

# =========================
# FLUTTER / JSON VIEWS
# =========================

@csrf_exempt
def create_event_flutter(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "User belum login"}, status=403)

    try:
        data = request.POST
        skor_h = data.get("skor_home")
        skor_a = data.get("skor_away")

        # 🔥 KRUSIAL: Jika Flutter kirim string kosong "", jadikan None
        skor_home = int(skor_h) if skor_h and skor_h.strip() != "" else None
        skor_away = int(skor_a) if skor_a and skor_a.strip() != "" else None

        tim_home = strip_tags(data.get("tim_home", ""))
        tim_away = strip_tags(data.get("tim_away", ""))
        nama_event = f"{tim_home} vs {tim_away}" if tim_home and tim_away else "Event Tanpa Nama"

        event = Event.objects.create(
            nama_event=nama_event,
            lokasi=strip_tags(data.get("lokasi", "")),
            tanggal=data.get("tanggal") if data.get("tanggal") else None,
            tim_home=tim_home,
            tim_away=tim_away,
            skor_home=skor_home,
            skor_away=skor_away,
            created_by=request.user
        )
        return JsonResponse({"status": "success", "message": "Event created", "id": event.id})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
def edit_event_flutter(request, pk):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    event = get_object_or_404(Event, pk=pk)
    if not (request.user == event.created_by or request.user.is_staff):
        return JsonResponse({"status": "error", "message": "Forbidden"}, status=403)

    data = request.POST
    skor_h = data.get("skor_home")
    skor_a = data.get("skor_away")

    event.lokasi = strip_tags(data.get("lokasi", event.lokasi))
    event.tanggal = data.get("tanggal", event.tanggal)
    event.tim_home = strip_tags(data.get("tim_home", event.tim_home))
    event.tim_away = strip_tags(data.get("tim_away", event.tim_away))
    
    # Update skor (handle nullable)
    event.skor_home = int(skor_h) if skor_h and skor_h.strip() != "" else None
    event.skor_away = int(skor_a) if skor_a and skor_a.strip() != "" else None

    event.nama_event = f"{event.tim_home} vs {event.tim_away}"
    event.save()
    return JsonResponse({"status": "success", "message": "Event updated"})

@csrf_exempt
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        if not (request.user == event.created_by or request.user.is_staff):
            return JsonResponse({"status": "error", "message": "Forbidden"}, status=403)
        event.delete()
        return JsonResponse({"status": "success", "message": "Event deleted"})
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

def show_event_json(request):
    """Menampilkan semua event dengan username pembuatnya."""
    data_event = Event.objects.all().order_by('-tanggal')
    result = []
    for event in data_event:
        result.append({
            "pk": event.pk,
            "fields": {
                "nama_event": event.nama_event,
                "lokasi": event.lokasi,
                "tanggal": event.tanggal,
                "tim_home": event.tim_home,
                "tim_away": event.tim_away,
                "skor_home": event.skor_home,
                "skor_away": event.skor_away,
                "username": event.created_by.username if event.created_by else "Unknown", 
            }
        })
    return JsonResponse(result, safe=False)

@csrf_exempt
def my_events_json(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Not authenticated"}, status=403)

    # Ambil event milik user yang sedang login
    events = Event.objects.filter(created_by=request.user).order_by('-tanggal')
    
    result = []
    for event in events:
        result.append({
            "model": "vidia_event.event", # Sesuai default model Flutter kamu
            "pk": event.pk,
            "fields": {
                "nama_event": event.nama_event,
                "lokasi": event.lokasi,
                "tanggal": event.tanggal.isoformat(),
                "tim_home": event.tim_home,
                "tim_away": event.tim_away,
                "skor_home": event.skor_home, # Bisa null
                "skor_away": event.skor_away, # Bisa null
                "created_by": event.created_by.id if event.created_by else None,
                "username": request.user.username, 
            }
        })

    return JsonResponse(result, safe=False)
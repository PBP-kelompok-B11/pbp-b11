from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, FileResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from authentication.views import admin_only
from comments.models import Comments
from comments.forms import CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.conf import settings
import json
import os

# =========================
# FLUTTER / JSON VIEWS
# =========================

@csrf_exempt
def show_event_json(request):
    """Menampilkan semua event dalam format JSON."""
    events = Event.objects.all().order_by('-tanggal')
    result = []
    for event in events:
        result.append({
            "model": "vidia_event.event",
            "pk": event.pk,
            "fields": {
                "nama_event": event.nama_event,
                "lokasi": event.lokasi,
                "tanggal": event.tanggal.isoformat() if event.tanggal else None,
                "tim_home": event.tim_home,
                "tim_away": event.tim_away,
                "skor_home": event.skor_home,
                "skor_away": event.skor_away,
                # Pastikan ini mengambil string URL
                "logo_home": str(event.logo_home) if event.logo_home else "", 
                "logo_away": str(event.logo_away) if event.logo_away else "",
                "username": event.created_by.username if event.created_by else "Unknown",
            }
        })
    return JsonResponse(result, safe=False)

@csrf_exempt
def my_events_json(request):
    """Menampilkan event milik user yang sedang login."""
    # Gunakan CookieRequest dari Flutter, biasanya user sudah terautentikasi
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Not authenticated"}, status=403)

    events = Event.objects.filter(created_by=request.user).order_by('-tanggal')
    result = []
    
    for event in events:
        result.append({
            "model": "vidia_event.event",
            "pk": event.pk,
            "fields": {
                "nama_event": event.nama_event,
                "lokasi": event.lokasi,
                "tanggal": event.tanggal.isoformat() if event.tanggal else None,
                "tim_home": event.tim_home,
                "tim_away": event.tim_away,
                "skor_home": event.skor_home,
                "skor_away": event.skor_away,
                # Pastikan logo dikirim sebagai string URL
                "logo_home": str(event.logo_home) if event.logo_home else "",
                "logo_away": str(event.logo_away) if event.logo_away else "",
                # Konsistensi dengan show_event_json
                "username": request.user.username, 
            }
        })
    return JsonResponse(result, safe=False)

@csrf_exempt
def club_logo(request, filename):
    """Mengambil file logo dari folder static/logos/ (Fallback)."""
    file_path = os.path.join(settings.BASE_DIR, 'static', 'logos', filename)
    if not os.path.exists(file_path):
        raise Http404("Logo not found")
    return FileResponse(open(file_path, 'rb'), content_type='image/png')

# =========================
# WEB VIEWS
# =========================

from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Event

# 1. KHUSUS UNTUK WEB (Mirip club_list kamu)
def event_list(request):
    events = Event.objects.all().order_by('-tanggal')
    
    # Menambahkan Paginator agar tampilan web tidak kepanjangan
    paginator = Paginator(events, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'base_title': 'Daftar Event',
    }
    return render(request, 'event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Logika untuk Flutter (JSON)
    if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
        return JsonResponse({
            "pk": event.pk,
            "nama_event": event.nama_event,
            "lokasi": event.lokasi,
            "tanggal": event.tanggal.isoformat() if event.tanggal else None,
            "tim_home": event.tim_home,
            "tim_away": event.tim_away,
            "skor_home": event.skor_home,
            "skor_away": event.skor_away,
            "logo_home": event.logo_home,
            "logo_away": event.logo_away,
        })

    # Logika untuk Web (HTML)
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
        
        event = Event.objects.create(
            nama_event=f"{request.POST.get('tim_home')} vs {request.POST.get('tim_away')}",
            lokasi=strip_tags(request.POST.get('lokasi', '')),
            tanggal=request.POST.get('tanggal') or None,
            tim_home=strip_tags(request.POST.get('tim_home', '')),
            tim_away=strip_tags(request.POST.get('tim_away', '')),
            skor_home=int(skor_h) if skor_h and skor_h.strip() != "" else None,
            skor_away=int(skor_a) if skor_a and skor_a.strip() != "" else None,
            logo_home=request.POST.get('logo_home'),
            logo_away=request.POST.get('logo_away'),
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
        event.lokasi = strip_tags(request.POST.get('lokasi', event.lokasi))
        event.tanggal = request.POST.get('tanggal', event.tanggal)
        event.tim_home = strip_tags(request.POST.get('tim_home', event.tim_home))
        event.tim_away = strip_tags(request.POST.get('tim_away', event.tim_away))
        event.logo_home = request.POST.get('logo_home', event.logo_home)
        event.logo_away = request.POST.get('logo_away', event.logo_away)
        
        skor_h = request.POST.get('skor_home')
        skor_a = request.POST.get('skor_away')
        event.skor_home = int(skor_h) if skor_h and skor_h.strip() != "" else None
        event.skor_away = int(skor_a) if skor_a and skor_a.strip() != "" else None

        event.nama_event = f"{event.tim_home} vs {event.tim_away}"
        event.save()
        return redirect('vidia_event:event_detail', pk=event.pk)
    return render(request, 'event_create.html', {'is_update': True, 'event': event})

# =========================
# FLUTTER ACTIONS
# =========================

@csrf_exempt
def create_event_flutter(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
    
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        skor_h = data.get("skor_home")
        skor_a = data.get("skor_away")
        
        event = Event.objects.create(
            nama_event=f"{data.get('tim_home')} vs {data.get('tim_away')}",
            lokasi=strip_tags(data.get("lokasi", "")),
            tanggal=data.get("tanggal") or None,
            tim_home=strip_tags(data.get("tim_home", "")),
            tim_away=strip_tags(data.get("tim_away", "")),
            skor_home=int(skor_h) if skor_h and str(skor_h).strip() != "" else None,
            skor_away=int(skor_a) if skor_a and str(skor_a).strip() != "" else None,
            logo_home=data.get("logo_home"),
            logo_away=data.get("logo_away"),
            created_by=request.user if request.user.is_authenticated else None
        )
        return JsonResponse({"status": "success", "message": "Event created"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
def edit_event_flutter(request, pk):
    """Mengedit event dari Flutter."""
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    event = get_object_or_404(Event, pk=pk)
    if not (request.user == event.created_by or request.user.is_staff):
        return JsonResponse({"status": "error", "message": "Forbidden"}, status=403)

    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        
        event.lokasi = strip_tags(data.get("lokasi", event.lokasi))
        event.tanggal = data.get("tanggal", event.tanggal)
        event.tim_home = strip_tags(data.get("tim_home", event.tim_home))
        event.tim_away = strip_tags(data.get("tim_away", event.tim_away))
        event.logo_home = data.get("logo_home", event.logo_home)
        event.logo_away = data.get("logo_away", event.logo_away)

        skor_h = data.get("skor_home")
        skor_a = data.get("skor_away")
        event.skor_home = int(skor_h) if skor_h and str(skor_h).strip() != "" else None
        event.skor_away = int(skor_a) if skor_a and str(skor_a).strip() != "" else None

        event.nama_event = f"{event.tim_home} vs {event.tim_away}"
        event.save()
        return JsonResponse({"status": "success", "message": "Event updated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
def event_delete(request, pk):
    """Menghapus event (bisa dari Web maupun Flutter)."""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        if not (request.user == event.created_by or request.user.is_staff):
            return JsonResponse({"status": "error", "message": "Forbidden"}, status=403)
        event.delete()
        return JsonResponse({"status": "success", "message": "Event deleted"})
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)
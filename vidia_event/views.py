from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import EventForm
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from authentication.views import admin_only
from comments.models import Comments
from comments.forms import CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import json


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
    print("DEBUG EVENT DETAIL:", event.nama_event, event.lokasi)
    return render(request, 'event_detail.html', {
        'event': event,
        'comments': comments,
        'form': form,
    })


@login_required(login_url='/authentication/login/')
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
        Event.objects.create(
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


@login_required(login_url='/authentication/login/')
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


@login_required(login_url='/authentication/login/')
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('vidia_event:event_list')
    return render(request, 'event_delete.html', {'event': event})


def show_event_json(request):
    """Mengembalikan daftar semua event dalam format JSON yang valid."""
    
    data_event = Event.objects.all().order_by('-tanggal')
    
    # 1. Serialisasi QuerySet menjadi string JSON
    json_string = serializers.serialize('json', data_event)
    
    # 2. Parsing string JSON kembali menjadi list Python/Dict
    # This ensures the output is a native Python structure.
    data_list = json.loads(json_string) 
    
    # 3. Kembalikan respons. JsonResponse will automatically handle
    # the list/dict and set the Content-Type header correctly.
    # No need for safe=False if the top-level object is a list (which it is here).
    return JsonResponse(data_list, safe=False)

@login_required(login_url='/authentication/login/')
def my_events_json(request):
    # Ambil semua event yang dibuat user yang login
    events = Event.objects.filter(created_by=request.user).order_by('-tanggal')

    # Serialisasi queryset ke JSON
    data = serializers.serialize('json', events)

    # Parse string JSON jadi Python list/dict agar JsonResponse valid
    import json
    data_list = json.loads(data)

    return JsonResponse(data_list, safe=False)

#tambahan
@login_required(login_url='/authentication/login')
def show_user_products(request):
    """
    Menampilkan daftar produk yang hanya dibuat oleh pengguna yang sedang login.
    """
    # 1. Menggunakan .filter(user=request.user) untuk mengambil hanya produk milik user
    event_list = Event.objects.filter(user=request.user)
    
    context = {
        'app' : 'Snitch Football',
        'name': 'Vidia Qonita Ahmad',
        'npm' : '2406345381',
        'class': 'PBP B',
        'product_list': event_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
        # Tambahkan flag untuk membedakan tampilan (jika diperlukan di template)
        'is_user_view': True,
    }

    # Anda bisa menggunakan template yang sama jika strukturnya cocok
    return render(request, "main.html", context)
@login_required(login_url='/authentication/login')
def show_json_user_products(request):
    """
    Mengembalikan data produk dalam format JSON, HANYA untuk user yang login.
    """
    # Filter produk hanya milik user yang sedang login
    event_list = Event.objects.filter(user=request.user)
    
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
        }
        for product in event_list
    ]

    return JsonResponse(data, safe=False)

@csrf_exempt
def create_event_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        lokasi = strip_tags(data.get('lokasi', ''))
        tanggal = data.get('tanggal', None)  # string date, boleh None
        tim_home = strip_tags(data.get('tim_home', ''))
        tim_away = strip_tags(data.get('tim_away', ''))
        skor_home = data.get('skor_home', None)
        skor_away = data.get('skor_away', None)

        # Sama seperti function create biasa
        if tim_home and tim_away:
            nama_event = f"{tim_home} vs {tim_away}"
        else:
            nama_event = "Event Tanpa Nama"

        # Buat objek event baru
        event = Event.objects.create(
            nama_event=nama_event,
            lokasi=lokasi,
            tanggal=tanggal if tanggal else None,
            tim_home=tim_home,
            tim_away=tim_away,
            skor_home=int(skor_home) if skor_home not in [None, ""] else None,
            skor_away=int(skor_away) if skor_away not in [None, ""] else None,
            created_by=request.user
        )

        return JsonResponse({"status": "success", "id": event.id}, status=200)

    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

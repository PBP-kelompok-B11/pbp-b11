from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .models import SearchQuery
from rafi_player.models import Player
from ibeth_clubs.models import Club
from vidia_event.models import Event


# ===============================
# SERIALIZATION (JSON & XML)
# ===============================

def show_json(request):
    """Menampilkan semua data SearchQuery dalam format JSON."""
    news_list = SearchQuery.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")


def show_xml_by_id(request, news_id):
    """Menampilkan satu data SearchQuery berdasarkan ID dalam format XML."""
    try:
        news_item = SearchQuery.objects.filter(pk=news_id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except SearchQuery.DoesNotExist:
        return HttpResponse(status=404)


# ===============================
# SEARCH PLAYERS (AJAX)
# ===============================

def search_players(request):
    """Mencari pemain berdasarkan nama, posisi, klub, atau negara (AJAX support)."""
    query = request.GET.get('q', '')
    results = []

    if query:
        SearchQuery.objects.create(
            user=request.user if request.user.is_authenticated else None,
            kata_kunci=query,
            jenis='pemain',
            tanggal=timezone.now()
        )

        results = Player.objects.filter(
            Q(nama__icontains=query) |
            Q(posisi__icontains=query) |
            Q(negara__icontains=query) |
            Q(careerhistory__klub__nama__icontains=query)
        ).distinct()

    # AJAX response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'nama': p.nama,
                'posisi': p.posisi,
                'negara': p.negara,
                'usia': getattr(p, 'usia', None)
            } for p in results
        ]
        return JsonResponse({'query': query, 'results': data, 'jenis': 'pemain'})

    # Fallback HTML
    return render(request, 'search/results.html', {'query': query, 'results': results, 'jenis': 'pemain'})


# ===============================
# FILTER PLAYERS (AJAX)
# ===============================

def filter_players(request):
    """Filter pemain dengan AJAX (posisi, negara, usia_min, usia_max)."""
    posisi_filter = request.GET.get('posisi', '')
    negara_filter = request.GET.get('negara', '')
    usia_min = request.GET.get('usia_min', '')
    usia_max = request.GET.get('usia_max', '')

    results = Player.objects.all()

    if posisi_filter:
        results = results.filter(posisi__iexact=posisi_filter)
    if negara_filter:
        results = results.filter(negara__iexact=negara_filter)
    if usia_min:
        results = results.filter(usia__gte=usia_min)
    if usia_max:
        results = results.filter(usia__lte=usia_max)

    results = results.distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'nama': p.nama,
                'posisi': p.posisi,
                'negara': p.negara,
                'usia': getattr(p, 'usia', None),
            } for p in results
        ]
        return JsonResponse({'results': data})

    return render(request, 'search/filter_results.html', {'results': results})


# ===============================
# SEARCH CLUBS (AJAX)
# ===============================

def search_clubs(request):
    """Mencari klub sepak bola berdasarkan nama atau negara (AJAX support)."""
    query = request.GET.get('q', '')
    results = []

    if query:
        SearchQuery.objects.create(
            user=request.user if request.user.is_authenticated else None,
            kata_kunci=query,
            jenis='klub',
            tanggal=timezone.now()
        )

        results = Club.objects.filter(
            Q(nama__icontains=query) |
            Q(negara__icontains=query)
        ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'nama': c.nama,
                'negara': c.negara,
                'liga': getattr(c, 'liga', None),
                'tahun_didirikan': getattr(c, 'tahun_didirikan', None),
            } for c in results
        ]
        return JsonResponse({'query': query, 'results': data, 'jenis': 'klub'})

    return render(request, 'search/results.html', {'query': query, 'results': results, 'jenis': 'klub'})


# ===============================
# FILTER CLUBS (AJAX)
# ===============================

def filter_clubs(request):
    """Filter klub sepak bola (negara, liga, tahun_didirikan) pakai AJAX."""
    negara_filter = request.GET.get('negara', '')
    liga_filter = request.GET.get('liga', '')
    tahun_filter = request.GET.get('tahun_didirikan', '')

    results = Club.objects.all()

    if negara_filter:
        results = results.filter(negara__iexact=negara_filter)
    if liga_filter:
        results = results.filter(liga__icontains=liga_filter)
    if tahun_filter:
        results = results.filter(tahun_didirikan__gte=tahun_filter)

    results = results.distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'nama': c.nama,
                'negara': c.negara,
                'liga': getattr(c, 'liga', None),
                'tahun_didirikan': getattr(c, 'tahun_didirikan', None),
            } for c in results
        ]
        return JsonResponse({'results': data})

    return render(request, 'search/filter_clubs.html', {'results': results})


# ===============================
# SEARCH HISTORY (AJAX)
# ===============================

@login_required
def search_history(request):
    """Menampilkan riwayat pencarian user (AJAX support)."""
    history = SearchQuery.objects.filter(user=request.user).order_by('-tanggal')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'kata_kunci': h.kata_kunci,
                'jenis': h.jenis,
                'tanggal': h.tanggal.strftime("%Y-%m-%d %H:%M"),
            } for h in history
        ]
        return JsonResponse({'history': data})

    return render(request, 'search/history.html', {'histories': history})



# ===============================
# SEARCH FORM
# ===============================

def search_form(request):
    """Menampilkan halaman form pencarian."""
    return render(request, 'search/form.html')

def search_redirect(request):
    query = request.GET.get('q', '').strip().lower()

    if not query:
        return redirect('home')  # atau halaman default

    # cek apakah keyword lebih cocok ke player atau club
    if Player.objects.filter(name__icontains=query).exists():
        return redirect(f'/player/?q={query}')
    elif Club.objects.filter(name__icontains=query).exists():
        return redirect(f'/club/?q={query}')
    else:
        # fallback kalau gak nemu apa pun
        return redirect('home')
    
@login_required
def clear_search_history(request):
    if request.method == 'POST':
        SearchQuery.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

# ===============================
# SEARCH EVENTS (AJAX)
# ===============================

def search_events(request):
    """Mencari event berdasarkan nama, tipe, atau lokasi (AJAX support)."""
    query = request.GET.get('q', '')
    results = []

    if query:
        # Simpan query ke database
        SearchQuery.objects.create(
            user=request.user if request.user.is_authenticated else None,
            kata_kunci=query,
            jenis='event',
            tanggal=timezone.now()
        )

        # Cari di model Event
        results = Event.objects.filter(
            Q(nama_event__icontains=query) |
            Q(tipe__icontains=query) |
            Q(lokasi__icontains=query)
        ).distinct()

    # Balikkan hasil ke AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'nama_event': e.nama_event,
                'tipe': e.tipe,
                'lokasi': e.lokasi,
                'tanggal_mulai': e.tanggal_mulai.strftime("%d %b %Y"),
                'tanggal_selesai': e.tanggal_selesai.strftime("%d %b %Y"),
            } for e in results
        ]
        return JsonResponse({'query': query, 'results': data, 'jenis': 'event'})

    # fallback ke HTML biasa
    return render(request, 'search/results.html', {
        'query': query,
        'results': results,
        'jenis': 'event'
    })


# ===============================
# FILTER EVENTS (AJAX)
# ===============================

def filter_events(request):
    """Filter event berdasarkan tipe, lokasi, atau rentang tanggal."""
    tipe_filter = request.GET.get('tipe', '')
    lokasi_filter = request.GET.get('lokasi', '')
    mulai_filter = request.GET.get('tanggal_mulai', '')
    selesai_filter = request.GET.get('tanggal_selesai', '')

    results = Event.objects.all()

    if tipe_filter:
        results = results.filter(tipe__iexact=tipe_filter)
    if lokasi_filter:
        results = results.filter(lokasi__icontains=lokasi_filter)
    if mulai_filter:
        results = results.filter(tanggal_mulai__gte=mulai_filter)
    if selesai_filter:
        results = results.filter(tanggal_selesai__lte=selesai_filter)

    results = results.distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'nama_event': e.nama_event,
                'tipe': e.tipe,
                'lokasi': e.lokasi,
                'tanggal_mulai': e.tanggal_mulai.strftime("%d %b %Y"),
                'tanggal_selesai': e.tanggal_selesai.strftime("%d %b %Y"),
            } for e in results
        ]
        return JsonResponse({'results': data})

    return render(request, 'search/filter_events.html', {'results': results})

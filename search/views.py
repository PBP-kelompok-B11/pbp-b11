from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .models import SearchQuery
from rafi_player.models import Player
from ibeth_clubs.models import Club


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

    return render(request, 'search/history.html', {'history': history})


# ===============================
# SEARCH FORM
# ===============================

def search_form(request):
    """Menampilkan halaman form pencarian."""
    return render(request, 'search/form.html')

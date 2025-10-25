# search/views.py
from urllib.parse import quote_plus
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.urls import reverse
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
    news_list = SearchQuery.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")


def show_xml_by_id(request, news_id):
    try:
        news_item = SearchQuery.objects.filter(pk=news_id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except SearchQuery.DoesNotExist:
        return HttpResponse(status=404)


# ===============================
# SEARCH PLAYERS (AJAX + HTML fallback -> rafi_player/list.html)
# ===============================
def search_players(request):
    query = request.GET.get('q', '').strip()
    results = Player.objects.none()

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

    # AJAX JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'id' : p.id,
                'nama': p.nama,
                'posisi': p.posisi,
                'negara': p.negara,
                'usia': getattr(p, 'usia', None)
            } for p in results
        ]
        return JsonResponse({'query': query, 'results': data, 'jenis': 'pemain'})

    # HTML fallback -> render ke template list players
    return render(request, 'player_list.html', {
        'query': query,
        'players': results,
        'jenis': 'pemain'
    })


# ===============================
# FILTER PLAYERS (AJAX)
# ===============================
def filter_players(request):
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
                'id' : p.id,
                'nama': p.nama,
                'posisi': p.posisi,
                'negara': p.negara,
                'usia': getattr(p, 'usia', None),
            } for p in results
        ]
        return JsonResponse({'results': data})

    return render(request, 'search/player_filter_component.html', {'results': results})


# ===============================
# SEARCH CLUBS (AJAX + HTML fallback -> ibeth_clubs/list.html)
# ===============================
def search_clubs(request):
    query = request.GET.get('q', '').strip()
    results = Club.objects.none()

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
                'id' : c.id,
                'nama': c.nama,
                'negara': c.negara,
                'liga': getattr(c, 'liga', None),
                'tahun_didirikan': getattr(c, 'tahun_didirikan', None),
            } for c in results
        ]
        return JsonResponse({'query': query, 'results': data, 'jenis': 'klub'})

    return render(request, 'clubs/list.html', {
        'query': query,
        'clubs': results,
        'jenis': 'klub'
    })


# ===============================
# FILTER CLUBS (AJAX)
# ===============================
def filter_clubs(request):
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
                'id' : c.id,
                'nama': c.nama,
                'negara': c.negara,
                'liga': getattr(c, 'liga', None),
                'tahun_didirikan': getattr(c, 'tahun_didirikan', None),
            } for c in results
        ]
        return JsonResponse({'results': data})

    return render(request, 'search/club_filter_component.html', {'results': results})


# ===============================
# SEARCH HISTORY (AJAX)
# ===============================
@login_required
def search_history(request):
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
    return render(request, 'search/form.html')


# ===============================
# REDIRECT FORM -> endpoint search (players|clubs|events)
# ===============================
def search_redirect(request):
    query = request.GET.get('q', '').strip()
    typ = request.GET.get('type', 'players').lower().strip()

    if not query:
        return redirect('search:search_form')

    if typ == 'players':
        target = reverse('search:search_players')   # -> /search/players/
    elif typ == 'clubs':
        target = reverse('search:search_clubs')     # -> /search/clubs/
    elif typ == 'events':
        target = reverse('search:search_events')    # -> /search/events/
    else:
        target = reverse('search:search_players')

    target += f'?q={quote_plus(query)}'
    return redirect(target)


@login_required
def clear_search_history(request):
    if request.method == 'POST':
        SearchQuery.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


# ===============================
# SEARCH EVENTS (AJAX + HTML fallback -> vidia_event/list.html)
# ===============================
def search_events(request):
    query = request.GET.get('q', '').strip()
    results = Event.objects.none()

    if query:
        SearchQuery.objects.create(
            user=request.user if request.user.is_authenticated else None,
            kata_kunci=query,
            jenis='event',
            tanggal=timezone.now()
        )

        results = Event.objects.filter(
            Q(nama_event__icontains=query) |
            Q(tipe__icontains=query) |
            Q(lokasi__icontains=query)
        ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'id': e.id,  
                'nama_event': e.nama_event,
                'tipe': e.tipe,
                'lokasi': e.lokasi,
                'tanggal_mulai': e.tanggal_mulai.strftime("%d %b %Y") if e.tanggal_mulai else None,
                'tanggal_selesai': e.tanggal_selesai.strftime("%d %b %Y") if e.tanggal_selesai else None,
            } for e in results
        ]
        return JsonResponse({'query': query, 'results': data, 'jenis': 'event'})

    return render(request, 'vidia_event/event_list.html', {
        'query': query,
        'events': results,
        'jenis': 'event'
    })


# ===============================
# FILTER EVENTS (AJAX)
# ===============================
def filter_events(request):
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
                'id': e.id,  
                'nama_event': e.nama_event,
                'tipe': e.tipe,
                'lokasi': e.lokasi,
                'tanggal_mulai': e.tanggal_mulai.strftime("%d %b %Y") if e.tanggal_mulai else None,
                'tanggal_selesai': e.tanggal_selesai.strftime("%d %b %Y") if e.tanggal_selesai else None,
            } for e in results
        ]
        return JsonResponse({'results': data})

    return render(request, 'search/event_filter_component.html', {'results': results})

import json
from urllib.parse import quote_plus
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator

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
# REDIRECT FORM -> endpoint search (players|clubs|events)
# ===============================
def search_redirect(request):
    query = request.GET.get('q', '').strip()
    typ = request.GET.get('type', 'players').lower().strip()

    if not query:
        return redirect('search:search_form')

    if typ == 'players':
        target = reverse('search:search_players')
    elif typ == 'clubs':
        target = reverse('search:search_clubs')
    elif typ == 'events':
        target = reverse('search:search_events')
    else:
        target = reverse('search:search_players')

    target += f'?q={quote_plus(query)}'
    return redirect(target)

# ===============================
# SEARCH PLAYERS
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
            Q(negara__icontains=query)
        ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {'id': str(p.id),
            'nama': p.nama,
            'posisi': p.posisi,
            'negara': p.negara,
            'usia': getattr(p, 'usia', None),
            'detail_url': reverse('rafi_player:player_detail', args=[str(p.id)]))}
            for p in results
        ]
        return JsonResponse({'query': query, 'results': data, 'jenis': 'pemain'})

    return render(request, 'player_list.html', {'query': query, 'players': results, 'jenis': 'pemain'})

# ===============================
# SEARCH CLUBS
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
            Q(negara__icontains=query) |
            Q(stadion__icontains=query)
        ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {'id': c.id, 'nama': c.nama, 'negara': c.negara, 'liga': getattr(c, 'liga', None),
             'tahun_didirikan': getattr(c, 'tahun_didirikan', None)}
            for c in results
        ]
        return JsonResponse({'query': query, 'results': data, 'jenis': 'klub'})
    print("Hasil klub:", results.count())


    return render(request, 'clubs/list.html', {'query': query, 'clubs': results, 'jenis': 'klub'})

# ===============================
# SEARCH EVENTS
# ===============================

def search_events(request):
    query = request.GET.get('q', '')
    events = Event.objects.filter(nama_event__icontains=query)

    print(f"Search events query: '{query}' -> jumlah hasil: {events.count()}")  # debug log

    if request.headers.get('x-requested-with', '').lower() == 'xmlhttprequest':
        data = {
            "results": [
                {
                    "id": e.id,
                    "nama_event": e.nama_event,
                    "tipe": getattr(e, 'tipe', ''),  
                    "lokasi": getattr(e, 'lokasi', ''),
                    "tanggal_mulai": getattr(e, 'tanggal_mulai', ''),
                    "tanggal_selesai": getattr(e, 'tanggal_selesai', ''),
                }
                for e in events
            ]
        }
        return JsonResponse(data)

    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "event_list.html",
        {
            "page_obj": page_obj,
            "query": query,
        },
    )

# ===============================
# SEARCH FORM
# ===============================
def search_form(request):
    return render(request, 'search/form.html')

#tes

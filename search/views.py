import json
from urllib.parse import quote_plus
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods

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
        news_item = SearchQuery.objects.get(pk=news_id)
        xml_data = serializers.serialize("xml", [news_item])
        return HttpResponse(xml_data, content_type="application/xml")
    except SearchQuery.DoesNotExist:
        return HttpResponse(status=404)


# ===============================
# REDIRECT FORM → search
# ===============================
def search_redirect(request):
    query = request.GET.get('q', '').strip()
    typ = request.GET.get('type', 'players').lower().strip()

    if not query:
        return redirect('search:search_form')

    target_map = {
        'players': 'search:search_players',
        'clubs': 'search:search_clubs',
        'events': 'search:search_events'
    }

    target = reverse(target_map.get(typ, 'search:search_players'))
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
            jenis='pemain'
        )
        results = Player.objects.filter(
            Q(nama__icontains=query) |
            Q(posisi__icontains=query) |
            Q(negara__icontains=query)
        ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'id': str(p.id),
                'nama': p.nama,
                'posisi': p.posisi,
                'negara': p.negara,
                'usia': getattr(p, 'usia', None),
                'detail_url': reverse('rafi_player:player_detail', args=[p.id])
            } for p in results
        ]
        return JsonResponse({'query': query, 'results': data})

    return render(request, 'player_list.html', {
        'query': query,
        'players': results,
    })


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
            jenis='klub'
        )
        results = Club.objects.filter(
            Q(nama__icontains=query) |
            Q(negara__icontains=query) |
            Q(stadion__icontains=query)
        ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'id': c.id,
                'nama': c.nama,
                'negara': c.negara,
                'liga': getattr(c, 'liga', None),
                'tahun_didirikan': getattr(c, 'tahun_didirikan', None),
            } for c in results
        ]
        return JsonResponse({'query': query, 'results': data})

    return render(request, 'clubs/list.html', {
        'query': query,
        'clubs': results,
    })


# ===============================
# SEARCH EVENTS
# ===============================
def search_events(request):
    query = request.GET.get('q', '')
    events = Event.objects.filter(nama_event__icontains=query)

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
                } for e in events
            ]
        }
        return JsonResponse(data)

    paginator = Paginator(events, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, "event_list.html", {
        "page_obj": page_obj,
        "query": query,
    })


# ===============================
# SEARCH FORM
# ===============================
def search_form(request):
    return render(request, 'search/form.html')


# ==============================================================
# 🚀 FLUTTER API - JSON ONLY
# ==============================================================

# Helper save history only if login
def save_history_if_login(request, query, jenis):
    if request.user.is_authenticated:
        SearchQuery.objects.create(
            user=request.user,
            kata_kunci=query,
            jenis=jenis
        )

# 🔍 API Search
def api_search(request):
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'players').lower()

    if not query:
        return JsonResponse({'error': 'q parameter required'}, status=400)

    if search_type == 'players':
        results = Player.objects.filter(
            Q(nama__icontains=query) |
            Q(posisi__icontains=query) |
            Q(negara__icontains=query)
        )
        jenis = 'pemain'
        data_key = 'players'
        data = [
            {"id": p.id, "nama": p.nama, "posisi": p.posisi, "negara": p.negara}
            for p in results
        ]

    elif search_type == 'clubs':
        results = Club.objects.filter(
            Q(nama__icontains=query) |
            Q(negara__icontains=query) |
            Q(stadion__icontains=query)
        )
        jenis = 'klub'
        data_key = 'clubs'
        data = [
            {"id": c.id, "nama": c.nama, "negara": c.negara}
            for c in results
        ]

    elif search_type == 'events':
        results = Event.objects.filter(
            nama_event__icontains=query
        )
        jenis = 'event'
        data_key = 'events'
        data = [
            {"id": e.id, "nama_event": e.nama_event}
            for e in results
        ]

    else:
        return JsonResponse({'error': 'Invalid type'}, status=400)

    save_history_if_login(request, query, jenis)

    return JsonResponse({
        "query": query,
        "type": search_type,
        "count": len(data),
        data_key: data
    })


# 📌 API Get History (ONLY LOGIN)
@login_required
def api_history(request):
    history = SearchQuery.objects.filter(user=request.user)
    data = [
        {
            "id": h.id,
            "kata_kunci": h.kata_kunci,
            "jenis": h.jenis,
            "tanggal": h.tanggal.isoformat(),
        } for h in history
    ]
    return JsonResponse({"history": data})


# ❌ Delete ALL History
@login_required
@require_http_methods(["DELETE"])
def api_history_clear(request):
    SearchQuery.objects.filter(user=request.user).delete()
    return JsonResponse({"message": "all history deleted"})


# ❌ Delete ONE History
@login_required
@require_http_methods(["DELETE"])
def api_history_delete_item(request, history_id):
    deleted, _ = SearchQuery.objects.filter(
        id=history_id, user=request.user
    ).delete()
    
    if deleted:
        return JsonResponse({"message": "history deleted", "id": history_id})

    return JsonResponse({"error": "not found"}, status=404)

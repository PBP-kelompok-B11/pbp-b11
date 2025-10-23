# search/views.py

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import SearchQuery
from rafi_player.models import Player
from clubs.models import Club
from django.core import serializers 

def show_xml_by_id(request, news_id):
   news_item = SearchQuery.objects.filter(pk=news_id)
   xml_data = serializers.serialize("xml", news_item)
   return HttpResponse(xml_data, content_type="application/xml")

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

def search_players(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # Simpan query ke database
        SearchQuery.objects.create(
            user=request.user if request.user.is_authenticated else None,
            kata_kunci=query,
            jenis='pemain',
            tanggal=timezone.now()
        )

        # Cari pemain berdasarkan nama, posisi, klub, atau negara
        results = Player.objects.filter(
            Q(nama__icontains=query) |
            Q(posisi__icontains=query) |
            Q(negara__icontains=query) |
            Q(careerhistory__klub__nama__icontains=query)
        ).distinct()

    # Kalau request-nya AJAX (fetch/axios/jQuery), kirim data JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'nama': p.nama,
                'negara': p.negara,
                'posisi': p.posisi,
                'usia': getattr(p, 'usia', None),
            }
            for p in results
        ]
        return JsonResponse({'results': data})

    # Kalau bukan AJAX, render halaman biasa
    context = {'query': query, 'results': results, 'jenis': 'pemain'}
    return render(request, 'search/results.html', context)


def search_clubs(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # Simpan query ke database
        SearchQuery.objects.create(
            user=request.user if request.user.is_authenticated else None,
            kata_kunci=query,
            jenis='klub',
            tanggal=timezone.now()
        )

        # Cari klub sepak bola
        results = Club.objects.filter(
            Q(nama__icontains=query) |
            Q(negara__icontains=query)
        ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'nama': c.nama,
                'negara': c.negara,
                'stadion': getattr(c, 'stadion', None),
            }
            for c in results
        ]
        return JsonResponse({'results': data})

    context = {'query': query, 'results': results, 'jenis': 'klub'}
    return render(request, 'search/results.html', context)


@login_required
def search_history(request):
    history = SearchQuery.objects.filter(user=request.user)
    return render(request, 'search/history.html', {'history': history})


def search_form(request):
    return render(request, 'search/form.html')

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Player
from .forms import PlayerForm

from django.http import JsonResponse
from .models import Player

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Player  # pastikan impor model Player

@csrf_exempt
@require_POST
def add_player_ajax(request):
    nama = request.POST.get("nama")
    negara = request.POST.get("negara")
    usia = request.POST.get("usia")
    tinggi = request.POST.get("tinggi")
    berat = request.POST.get("berat")
    posisi = request.POST.get("posisi")
    thumbnail= request.POST.get("thumbnail")

    # Validasi sederhana
    if not all([nama, negara, usia, tinggi, berat, posisi, thumbnail]):
        return HttpResponse(b"Missing fields", status=400)

    new_player = Player(
        nama=nama,
        negara=negara,
        usia=usia,
        tinggi=tinggi,
        berat=berat,
        posisi=posisi,
        thumbnail=thumbnail,
    )
    new_player.save()

    # Return JSON biar bisa ditangani di JS
    return HttpResponse(b"CREATED", status=201)

def show_json_player(request):
    player_list = Player.objects.all()
    data = [
        {
            'id': player.id,
            'nama': player.nama,
            'negara': player.negara,
            'usia': player.usia,
            'tinggi': player.tinggi,
            'berat': player.berat,
            'posisi': player.posisi,
            'thumbnail':player.thumbnail,
            'user_id': player.user_id,
        }
        for player in player_list
    ]

    return JsonResponse(data, safe=False)

def show_json_player_by_id(request, player_id):
    try:
        player = Player.objects.select_related('user').get(pk=player_id)
        data = {
            'id': str(player.id),
            'nama': player.nama,
            'negara': player.negara,
            'usia': player.usia,
            'tinggi': player.tinggi,
            'berat': player.berat,
            'posisi': player.posisi,
            'thumbnail':player.thumbnail,
            'user_id': player.user_id if hasattr(player, 'user_id') else None,
            'user_username': player.user.username if hasattr(player, 'user') and player.user else None,
        }
        return JsonResponse(data)
    except Player.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def player_detail(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    context = {
        'player': player,
        'player_id': player_id,  # <---- tambahkan baris ini
    }
    return render(request, 'player_details.html', context)

def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})

def player_create(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rafi_player:player_list')
    else:
        form = PlayerForm()
    return render(request, 'player_form.html', {'form': form})

def player_update(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('rafi_player:player_detail', pk=pk)
    else:
        form = PlayerForm(instance=player)
    return render(request, 'player_form.html', {'form': form})

def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk)
    player.delete()
    return redirect('rafi_player:player_list')

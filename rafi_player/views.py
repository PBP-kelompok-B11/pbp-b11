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
from .models import Player 

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from authentication.views import admin_only

@csrf_exempt
@login_required(login_url='/login/')
def add_player_ajax(request):
    print("DEBUG - User:", request.user)
    print("DEBUG - Authenticated:", request.user.is_authenticated)

    nama = request.POST.get("nama")
    negara = request.POST.get("negara")
    usia = request.POST.get("usia")
    tinggi = request.POST.get("tinggi")
    berat = request.POST.get("berat")
    posisi = request.POST.get("posisi")
    thumbnail= request.POST.get("thumbnail")

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
        user=request.user 
    )
    new_player.save()


    return JsonResponse({'message': 'CREATED'})

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

    achievements = player.prestasi.all()
    stats = player.statistik_musim.all()
    careers = player.riwayat_karier.all()

    return render(request, 'player_details.html', {
        'player_id': player_id,
        'player': player,
        'achievements': achievements,
        'stats': stats,
        'careers': careers,
    })

def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})

@login_required(login_url='/login/')
def player_create(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rafi_player:player_list')
    else:
        form = PlayerForm()
    return render(request, 'player_form.html', {'form': form})

@login_required(login_url='/login/')
def edit_player_ajax(request, pk):
    if request.method == 'POST':
        player = get_object_or_404(Player, pk=pk)
        player.nama = request.POST.get('nama')
        player.negara = request.POST.get('negara')
        player.usia = request.POST.get('usia')
        player.tinggi = request.POST.get('tinggi')
        player.berat = request.POST.get('berat')
        player.posisi = request.POST.get('posisi')
        player.thumbnail = request.POST.get('thumbnail')
        player.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

@require_POST
@login_required(login_url='/login/')    
def delete_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player.delete()
    return redirect('rafi_player:player_list') 

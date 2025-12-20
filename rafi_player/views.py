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
from comments.models import Comments
from comments.forms import CommentForm

from django.http import JsonResponse, HttpResponseNotAllowed

@csrf_exempt
@login_required(login_url='/login/')
@admin_only
def add_player_ajax(request):
    if request.method != "POST":
        return JsonResponse({'message': 'Invalid method'}, status=405)

    nama = request.POST.get("nama")
    negara = request.POST.get("negara")
    usia = request.POST.get("usia")
    tinggi = request.POST.get("tinggi")
    berat = request.POST.get("berat")
    posisi = request.POST.get("posisi")
    thumbnail = request.POST.get("thumbnail")

    if not all([nama, negara, usia, tinggi, berat, posisi, thumbnail]):
        return JsonResponse({'message': 'Missing fields'}, status=400)

    try:
        new_player = Player(
            nama=nama,
            negara=negara,
            usia=int(usia),
            tinggi=float(tinggi),
            berat=float(berat),
            posisi=posisi,
            thumbnail=thumbnail,
            user=request.user
        )
        new_player.save()
        return JsonResponse({'message': 'CREATED'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


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
    comments = Comments.objects.filter(
        content_type__model='player',
        object_id=player.id
    ).order_by('-tanggal')

    # Siapkan form komentar baru
    form = CommentForm()

    return render(request, 'player_details.html', {
        'player_id': player_id,
        'player': player,
        'achievements': achievements,
        'stats': stats,
        'careers': careers,
        'comments': comments,
        'form': form,
    })

def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})

@login_required(login_url='/login/')
@admin_only
def edit_player_ajax(request, pk):
    # console.log("edit dipanggil")
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
@admin_only  
def delete_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player.delete()
    return redirect('rafi_player:player_list') 

def player_detail_json(request, player_id):
    player = Player.objects.get(id=player_id)

    data = {
        "id": str(player.id),
        "nama": player.nama,
        "negara": player.negara,
        "usia": player.usia,
        "tinggi": player.tinggi,
        "berat": player.berat,
        "posisi": player.posisi,
        "thumbnail": player.thumbnail,
        # Achievement
        "achievement": [
            {"deskripsi": a.deskripsi, "tahun": a.tahun} 
            for a in player.prestasi.all()
        ],
        # Season Stats
        "season_stats": [
            {
                "musim": s.musim,
                "pertandingan": s.pertandingan,
                "gol": s.gol,
                "assist": s.assist,
                "kartu": s.kartu
            } 
            for s in player.statistik_musim.all()
        ],
        # Career History
        "career_history": [
            {
                "klub": c.klub,
                "tahun_mulai": c.tahun_mulai,
                "tahun_selesai": c.tahun_selesai
            } 
            for c in player.riwayat_karier.all()
        ],
    }
    return JsonResponse(data)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.html import strip_tags
import json
from .models import Player, Achievement, SeasonStats, CareerHistory
from django.contrib.auth.models import User

@csrf_exempt
def create_player_entry(request):
    # print("Data diterima:", data)
    print("USER:", request.user)                     
    print("AUTH:", request.user.is_authenticated)
    
    if request.method != 'POST':
        return JsonResponse(
            {"status": "error", "message": "Method not allowed"},
            status=405
        )

    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "Unauthorized"},
            status=401
        )

    try:
        
        if request.method == 'POST':
            data = json.loads(request.body)
            
            nama = strip_tags(data.get("nama", ""))
            negara = strip_tags(data.get("negara", ""))
            usia = data.get("usia", 0)
            tinggi = data.get("tinggi", 0)
            berat = data.get("berat", 0)
            posisi = data.get("posisi", "")
            thumbnail = data.get("thumbnail", "")

            # Jika kamu ingin created_at dari Flutter
            # created_at = data.get("created_at", None)

            player = Player(
                nama=nama,
                negara=negara,
                usia=usia,
                tinggi=tinggi,
                berat=berat,
                posisi=posisi,
                thumbnail=thumbnail,
                user=request.user,
            )

            # Achievement
            for ach in data.get("achievement", []):
                Achievement.objects.create(player=player, **ach)

            # Season stats
            for stat in data.get("season_stats", []):
                SeasonStats.objects.create(player=player, **stat)

            # Career history
            for career in data.get("career_history", []):
                CareerHistory.objects.create(player=player, **career)

            player.save()

            return JsonResponse({"status": "success"}, status=200)

        # return JsonResponse({"status": "success"}, status=200)
        
        else:
            return JsonResponse({"status": "error"}, status=401)


    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=400
        )

@csrf_exempt
def edit_player_entry(request, player_id):
    if request.method not in ["POST", "PUT"]:
        return HttpResponseNotAllowed(["POST", "PUT"])
    
    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return JsonResponse({"error": "Player not found"}, status=404)

    data = json.loads(request.body)

    player.nama = data.get("nama", player.nama)
    player.posisi = data.get("posisi", player.posisi)
    player.negara = data.get("negara", player.negara)
    player.tinggi = data.get("tinggi", player.tinggi)
    player.berat = data.get("berat", player.berat)
    player.usia = data.get("usia", player.usia)
    player.thumbnail = data.get("thumbnail", player.thumbnail)

    player.save()

    return JsonResponse({
        "message": "Player updated successfully"
    })


@csrf_exempt
def delete_player_entry(request, player_id):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return JsonResponse({"error": "Player not found"}, status=404)

    player.delete()

    return JsonResponse({
        "message": "Player deleted successfully"
    })


def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)

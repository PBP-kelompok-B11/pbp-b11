from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Player
from .forms import PlayerForm

def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})

def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'player_detail.html', {'player': player})

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

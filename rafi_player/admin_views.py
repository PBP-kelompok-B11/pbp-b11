# rafi_player/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Player
from .forms import PlayerForm
from django.contrib.auth.decorators import login_required

# LIST PLAYERS
@login_required
def player_list(request):
    players = Player.objects.all()
    return render(request, 'admin/player_list.html', {'players': players})

# ADD PLAYER
@login_required
def player_add(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            return redirect('rafi_player:admin_player_list')
    else:
        form = PlayerForm()
    return render(request, 'admin/player_form.html', {'form': form, 'title': 'Add Player'})

# EDIT PLAYER
@login_required
def player_edit(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('rafi_player:admin_player_list')
    else:
        form = PlayerForm(instance=player)
    return render(request, 'admin/player_form.html', {'form': form, 'title': 'Edit Player'})

# DELETE PLAYER
@login_required
def player_delete(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == 'POST':
        player.delete()
        return redirect('rafi_player:admin_player_list')
    return render(request, 'admin/player_confirm_delete.html', {'player': player})
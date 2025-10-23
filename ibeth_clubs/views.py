from django.shortcuts import render, redirect, get_object_or_404
from .models import Club, ClubRanking
from .forms import ClubForm, ClubRankingForm

def club_list(request):
    clubs = Club.objects.all().order_by('nama')
    return render(request, 'clubs/list.html', {'clubs': clubs})

def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    rankings = club.rankings.all().order_by('-musim')
    return render(request, 'clubs/detail.html', {'club': club, 'rankings': rankings})

def club_create(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save()
            return redirect('club_detail', pk=club.pk)
    else:
        form = ClubForm()
    return render(request, 'clubs/form.html', {'form': form, 'title': 'Add Club'})

def club_update(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            club = form.save()
            return redirect('club_detail', pk=club.pk)
    else:
        form = ClubForm(instance=club)
    return render(request, 'clubs/form.html', {'form': form, 'title': f'Edit Club: {club.nama}'})

def club_delete(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        club.delete()
        return redirect('club_list')
    return render(request, 'clubs/club_confirm_delete.html', {'club': club})

def ranking_list(request):
    rankings = ClubRanking.objects.select_related('club').order_by('club__nama', 'peringkat')
    return render(request, 'clubs/ranking.html', {'rankings': rankings})

def club_ranking_create(request, club_pk):
    club = get_object_or_404(Club, pk=club_pk)
    if request.method == 'POST':
        form = ClubRankingForm(request.POST)
        if form.is_valid():
            ranking = form.save(commit=False)
            ranking.club = club
            ranking.save()
            return redirect('club_detail', pk=club.pk)
    else:
        form = ClubRankingForm()
    return render(request, 'clubs/form.html', {'form': form, 'title': f'Add Ranking for {club.nama}'})

def club_ranking_update(request, pk):
    ranking = get_object_or_404(ClubRanking, pk=pk)
    if request.method == 'POST':
        form = ClubRankingForm(request.POST, instance=ranking)
        if form.is_valid():
            form.save()
            return redirect('club_detail', pk=ranking.club.pk)
    else:
        form = ClubRankingForm(instance=ranking)
    return render(request, 'clubs/form.html', {'form': form, 'title': f'Edit Ranking {ranking.club.nama} - {ranking.musim}'})

def club_ranking_delete(request, pk):
    ranking = get_object_or_404(ClubRanking, pk=pk)
    club_pk = ranking.club.pk
    if request.method == 'POST':
        ranking.delete()
        return redirect('club_detail', pk=club_pk)
    return render(request, 'clubs/ranking_confirm_delete.html', {'ranking': ranking})

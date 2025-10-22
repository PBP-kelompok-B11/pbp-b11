from django.shortcuts import render, get_object_or_404, redirect
from .models import Club, Ranking
from .forms import ClubForm, RankingForm


def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'clubs/list.html', {'clubs': clubs})


def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    rankings = club.rankings.all().order_by('musim')
    return render(request, 'clubs/detail.html', {'club': club, 'rankings': rankings})


def club_create(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('club_list')
    else:
        form = ClubForm()
    return render(request, 'clubs/form.html', {'form': form})


def club_update(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            return redirect('club_detail', pk=club.pk)
    else:
        form = ClubForm(instance=club)
    return render(request, 'clubs/form.html', {'form': form})


def club_delete(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        club.delete()
        return redirect('club_list')
    return render(request, 'clubs/club_confirm_delete.html', {'club': club})


def ranking_list(request):
    rankings = Ranking.objects.select_related('club').order_by('peringkat')
    return render(request, 'clubs/ranking.html', {'rankings': rankings})


def ranking_create(request, club_pk):
    club = get_object_or_404(Club, pk=club_pk)
    if request.method == 'POST':
        form = RankingForm(request.POST)
        if form.is_valid():
            ranking = form.save(commit=False)
            ranking.club = club
            ranking.save()
            return redirect('club_detail', pk=club.pk)
    else:
        form = RankingForm()
    return render(request, 'clubs/form.html', {'form': form})


def ranking_update(request, pk):
    ranking = get_object_or_404(Ranking, pk=pk)
    if request.method == 'POST':
        form = RankingForm(request.POST, instance=ranking)
        if form.is_valid():
            form.save()
            return redirect('club_detail', pk=ranking.club.pk)
    else:
        form = RankingForm(instance=ranking)
    return render(request, 'clubs/form.html', {'form': form})


def ranking_delete(request, pk):
    ranking = get_object_or_404(Ranking, pk=pk)
    if request.method == 'POST':
        club_pk = ranking.club.pk
        ranking.delete()
        return redirect('club_detail', pk=club_pk)
    return render(request, 'clubs/ranking_confirm_delete.html', {'ranking': ranking})

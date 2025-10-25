from django.shortcuts import render, redirect, get_object_or_404
from .models import Club, ClubRanking
from .forms import ClubForm, ClubRankingForm
from authentication.views import admin_only
from django.contrib.auth.decorators import login_required


def club_list(request):
    clubs = Club.objects.all().order_by('nama')
    context = {
        'clubs': clubs,
        'base_title': 'Daftar Klub',
    }
    return render(request, 'clubs/list.html', context)


def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    rankings = club.rankings.all().order_by('-musim')
    context = {
        'club': club,
        'rankings': rankings,
        'base_title': f'Detail {club.nama}',
    }
    return render(request, 'clubs/detail.html', context)

@login_required(login_url='/login/')
def club_create(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save()
            return redirect('ibeth_clubs:club_detail', pk=club.pk)
    else:
        form = ClubForm()

    context = {
        'form': form,
        'title': 'Tambah Klub',
        'base_title': 'Tambah Klub Baru',
    }
    return render(request, 'clubs/form.html', context)

@login_required(login_url='/login/')
def club_update(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            club = form.save()
            return redirect('ibeth_clubs:club_detail', pk=club.pk)
    else:
        form = ClubForm(instance=club)

    context = {
        'form': form,
        'title': f'Edit Klub: {club.nama}',
        'base_title': f'Edit Klub - {club.nama}',
    }
    return render(request, 'clubs/form.html', context)

@login_required(login_url='/login/')
def club_delete(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        club.delete()
        return redirect('ibeth_clubs:club_list')
    context = {
        'club': club,
        'base_title': f'Hapus Klub {club.nama}',
    }
    return render(request, 'clubs/club_confirm_delete.html', context)



def ranking_list(request):
    rankings = ClubRanking.objects.select_related('club').order_by('club__nama', 'peringkat')
    context = {
        'rankings': rankings,
        'base_title': 'Daftar Ranking Klub',
    }
    return render(request, 'clubs/ranking.html', context)

@login_required(login_url='/login/')
def club_ranking_create(request, club_pk):
    club = get_object_or_404(Club, pk=club_pk)
    if request.method == 'POST':
        form = ClubRankingForm(request.POST)
        if form.is_valid():
            ranking = form.save(commit=False)
            ranking.club = club
            ranking.save()
            return redirect('ibeth_clubs:club_detail', pk=club.pk)
    else:
        form = ClubRankingForm()

    context = {
        'form': form,
        'title': f'Tambah Ranking untuk {club.nama}',
        'base_title': f'Tambah Ranking - {club.nama}',
    }
    return render(request, 'clubs/form.html', context)

@login_required(login_url='/login/')
def club_ranking_update(request, pk):
    ranking = get_object_or_404(ClubRanking, pk=pk)
    if request.method == 'POST':
        form = ClubRankingForm(request.POST, instance=ranking)
        if form.is_valid():
            form.save()
            return redirect('ibeth_clubs:club_detail', pk=ranking.club.pk)
    else:
        form = ClubRankingForm(instance=ranking)

    context = {
        'form': form,
        'title': f'Edit Ranking {ranking.club.nama} - {ranking.musim}',
        'base_title': f'Edit Ranking - {ranking.club.nama}',
    }
    return render(request, 'clubs/form.html', context)

@login_required(login_url='/login/')
def club_ranking_delete(request, pk):
    ranking = get_object_or_404(ClubRanking, pk=pk)
    club_pk = ranking.club.pk
    if request.method == 'POST':
        ranking.delete()
        return redirect('ibeth_clubs:club_detail', pk=club_pk)

    context = {
        'ranking': ranking,
        'base_title': f'Hapus Ranking {ranking.club.nama}',
    }
    return render(request, 'clubs/ranking_confirm_delete.html', context)

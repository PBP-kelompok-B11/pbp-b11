from django.shortcuts import render, redirect, get_object_or_404
from .models import Club, ClubRanking
from .forms import ClubForm, ClubRankingForm
from django.contrib.auth.decorators import login_required
from comments.models import Comments
from comments.forms import CommentForm
from authentication.views import admin_only
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ClubSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ClubSerializer, ClubRankingSerializer

def club_list(request):
    clubs = Club.objects.all().order_by('nama')
    context = {
        'clubs': clubs,
        'base_title': 'Daftar Klub',
    }
    return render(request, 'clubs/list.html', context)


def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    rankings = ClubRanking.objects.filter(club=club).order_by('-musim')
    comments = Comments.objects.filter(
        content_type__model='club',
        object_id=club.id
    ).order_by('-tanggal')

    form = CommentForm()
    context = {
        'club': club,
        'rankings': rankings,
        'base_title': f'Detail {club.nama}',
        'comments': comments,
        'form': form,
    }
    return render(request, 'clubs/detail.html', context)


@login_required(login_url='/login/')
@admin_only
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
        'is_edit': False,
        'club': None,  
    }
    return render(request, 'clubs/form.html', context)


@login_required(login_url='/login/')
@admin_only
def club_update(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            return redirect('ibeth_clubs:club_detail', pk=club.pk)
    else:
        form = ClubForm(instance=club)

    context = {
        'form': form,
        'club': club,
        'is_edit': True,
    }
    return render(request, 'clubs/form.html', context)


@login_required(login_url='/login/')
@admin_only
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
@admin_only
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
@admin_only
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
@admin_only
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

@api_view(['GET'])
def api_club_list(request):
    clubs = Club.objects.all().order_by('nama')
    serializer = ClubSerializer(clubs, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def api_club_list_create(request):
    if request.method == 'GET':
        clubs = Club.objects.all()
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def api_club_detail(request, pk):
    try:
        club = Club.objects.get(pk=pk)
    except Club.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    # GET detail
    if request.method == 'GET':
        serializer = ClubSerializer(club)
        return Response(serializer.data)

    # PUT update
    if request.method == 'PUT':
        serializer = ClubSerializer(club, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # DELETE remove
    if request.method == 'DELETE':
        club.delete()
        return Response(status=204)
    
@api_view(['POST'])
def api_create_ranking(request, club_pk):
    try:
        club = Club.objects.get(pk=club_pk)
    except Club.DoesNotExist:
        return Response({'error': 'Club not found'}, status=404)

    serializer = ClubRankingSerializer(data=request.data)
    if serializer.is_valid():
        ranking = serializer.save(club=club)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


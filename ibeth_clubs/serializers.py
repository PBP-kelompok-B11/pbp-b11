from rest_framework import serializers
from .models import Club, ClubRanking

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            'id',
            'nama',
            'negara',
            'stadion',
            'tahun_berdiri',
            'url_gambar',
        ]

class ClubRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubRanking
        fields = [
            'id',
            'club',
            'musim',
            'peringkat',
        ]

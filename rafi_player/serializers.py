from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'id',
            'nama',
            'negara',
            'usia',
            'tinggi',
            'berat',
            'posisi',
            'thumbnail',
        ]
